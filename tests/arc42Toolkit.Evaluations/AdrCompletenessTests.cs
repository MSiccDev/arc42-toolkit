using System.Text.Json;
using System.Text.Json.Serialization;
using arc42Toolkit.Evaluations.Evaluators;
using Microsoft.Extensions.AI;
using Microsoft.Extensions.AI.Evaluation;
using Microsoft.Extensions.AI.Evaluation.Reporting;
using Microsoft.Extensions.AI.Evaluation.Reporting.Storage;
using OllamaSharp;

namespace arc42Toolkit.Evaluations.Tests;

public class AdrCompletenessTests
{
    // Resolves to tests/arc42Toolkit.Evaluations/eval-results
    private static readonly string ReportStoragePath = Path.Combine(
        AppContext.BaseDirectory, "..", "..", "..", "eval-results");

    private static readonly string TestDataPath = Path.Combine(AppContext.BaseDirectory, "TestData");

    // AppContext.BaseDirectory is tests/arc42Toolkit.Evaluations/bin/Debug/net10.0/;
    // five levels up lands at the repository root, so real (non-fixture) docs such as
    // docs/adrs/ can be referenced directly instead of being copied into TestData.
    private static readonly string RepoRootPath = Path.Combine(
        AppContext.BaseDirectory, "..", "..", "..", "..", "..");

    private static IChatClient CreateOllamaClient() =>
        new OllamaApiClient(
            // Default HttpClient timeout is 100s. A local reasoning-model judge can take
            // several minutes on a single ADR depending on prompt complexity — the
            // default was cutting off valid, still-in-progress responses.
            new HttpClient
            {
                BaseAddress = new Uri("http://localhost:11434"),
                Timeout = TimeSpan.FromMinutes(10)
            },
            defaultModel: "phi4-reasoning:14b-plus-q8_0");

    // Shared across all scenarios in this class so their results land under
    // the same execution and show up together in the generated report.  
    private static readonly ReportingConfiguration ReportingConfig =
    DiskBasedReportingConfiguration.Create(
        storageRootPath: ReportStoragePath,
        evaluators: [new AdrCompletenessEvaluator()],
        chatConfiguration: new ChatConfiguration(CreateOllamaClient()),
        executionName: $"{DateTime.Now:yyyyMMddTHHmmss}",
        enableResponseCaching: false);

    // Golden dataset fixtures — see TestData/golden-dataset.json and TestData/adrs/.
    // Each entry records the expected score band for a real or synthetic ADR, so this
    // one theory replaces what would otherwise be a hand-written fact per fixture.
    public static TheoryData<string, string, string, double, double> GoldenDataset()
    {
        string json = File.ReadAllText(Path.Combine(TestDataPath, "golden-dataset.json"));
        List<GoldenDatasetEntry> entries = JsonSerializer.Deserialize<List<GoldenDatasetEntry>>(json)
            ?? throw new InvalidOperationException("golden-dataset.json deserialized to null.");

        var data = new TheoryData<string, string, string, double, double>();
        foreach (GoldenDatasetEntry entry in entries)
        {
            data.Add(entry.Id, entry.File, entry.ExpectedLabel, entry.ExpectedScoreMin, entry.ExpectedScoreMax);
        }

        return data;
    }

    // Runs the full golden dataset against a slow-but-rigorous reasoning judge (~30 min
    // locally). Excluded from default runs via `dotnet test --filter "Category!=Slow"`;
    // run explicitly or in a scheduled job instead.
    [Theory]
    [Trait("Category", "Slow")]
    [MemberData(nameof(GoldenDataset))]
    public async Task AdrCompleteness_MatchesGoldenExpectation(
        string id, string file, string expectedLabel, double expectedScoreMin, double expectedScoreMax)
    {
        await using ScenarioRun scenarioRun = await ReportingConfig.CreateScenarioRunAsync(id);

        string adrText = await File.ReadAllTextAsync(Path.Combine(TestDataPath, file));
        var messages = new[] { new ChatMessage(ChatRole.User, "Evaluate this ADR.") };
        var response = new ChatResponse(new ChatMessage(ChatRole.Assistant, adrText));

        EvaluationResult result = await scenarioRun.EvaluateAsync(messages, response);

        var metric = result.Get<NumericMetric>(AdrCompletenessEvaluator.MetricName);

        Assert.True(metric.Value >= expectedScoreMin && metric.Value <= expectedScoreMax,
            $"[{id}] Expected a '{expectedLabel}' ADR to score within [{expectedScoreMin}, {expectedScoreMax}], " +
            $"got {metric.Value}. Reason: {metric.Interpretation?.Reason}");
    }

    // Demo-only single run against the toolkit's own real ADR (docs/adrs/), not a
    // TestData fixture and not part of the golden dataset. Not run by default — invoke
    // explicitly, e.g.:
    //   dotnet test --filter "Category=Demo"
    [Fact]
    [Trait("Category", "Demo")]
    public async Task AdrCompleteness_DemoRun_ExtractEvaluationToolAdr()
    {
        await using ScenarioRun scenarioRun =
            await ReportingConfig.CreateScenarioRunAsync(nameof(AdrCompleteness_DemoRun_ExtractEvaluationToolAdr));

        string adrPath = Path.Combine(
            RepoRootPath, "docs", "adrs",
            "ADR-0001-extract-ai-evaluation-prototype-into-a-distributable-net-cli-tool.md");
        string adrText = await File.ReadAllTextAsync(adrPath);
        var messages = new[] { new ChatMessage(ChatRole.User, "Evaluate this ADR.") };
        var response = new ChatResponse(new ChatMessage(ChatRole.Assistant, adrText));

        EvaluationResult result = await scenarioRun.EvaluateAsync(messages, response);

        var metric = result.Get<NumericMetric>(AdrCompletenessEvaluator.MetricName);

        Assert.True(metric.Value >= 0.8,
            $"Expected the toolkit's own extraction ADR to score >= 0.8, got {metric.Value}. " +
            $"Reason: {metric.Interpretation?.Reason}");
    }

    private sealed class GoldenDatasetEntry
    {
        [JsonPropertyName("id")]
        public string Id { get; init; } = string.Empty;

        [JsonPropertyName("file")]
        public string File { get; init; } = string.Empty;

        [JsonPropertyName("expectedLabel")]
        public string ExpectedLabel { get; init; } = string.Empty;

        [JsonPropertyName("expectedScoreMin")]
        public double ExpectedScoreMin { get; init; }

        [JsonPropertyName("expectedScoreMax")]
        public double ExpectedScoreMax { get; init; }
    }
}
