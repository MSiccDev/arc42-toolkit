using System.ClientModel;
using Arc42Toolkit.Evals.Evaluators;
using Microsoft.Extensions.AI;
using Microsoft.Extensions.AI.Evaluation;
using Microsoft.Extensions.AI.Evaluation.Reporting;
using Microsoft.Extensions.AI.Evaluation.Reporting.Storage;
using OpenAI;

namespace arc42Toolkit.Evaluations;

public class ArchitecturalRelevanceTests
{
    // Resolves to tests/arc42Toolkit.Evaluations/eval-results
    private static readonly string ReportStoragePath = Path.Combine(
        AppContext.BaseDirectory, "..", "..", "..", "eval-results");

    private static IChatClient CreateLmStudioClient() =>
        new OpenAIClient(
                new ApiKeyCredential("lm-studio"),
                new OpenAIClientOptions { Endpoint = new Uri("http://localhost:1234/v1") })
            .GetChatClient("microsoft/phi-4-reasoning-plus")
            .AsIChatClient();

    // Shared across all scenarios in this class so their results land under
    // the same execution and show up together in the generated report.
    private static readonly ReportingConfiguration ReportingConfig =
        DiskBasedReportingConfiguration.Create(
            storageRootPath: ReportStoragePath,
            evaluators: [new ArchitecturalRelevanceEvaluator()],
            chatConfiguration: new ChatConfiguration(CreateLmStudioClient()));

    // Calibration test #1 — a complete ADR should score well.
    // Use one of your real, well-formed ADRs here.
    [Fact]
    public async Task WellFormedAdr_ScoresHigh()
    {
        await using ScenarioRun scenarioRun =
            await ReportingConfig.CreateScenarioRunAsync(nameof(WellFormedAdr_ScoresHigh));

        string adrText = await File.ReadAllTextAsync("TestData/adr-001-good.md");
        var messages = new[] { new ChatMessage(ChatRole.User, "Evaluate this ADR.") };
        var response = new ChatResponse(new ChatMessage(ChatRole.Assistant, adrText));

        EvaluationResult result = await scenarioRun.EvaluateAsync(messages, response);

        var metric = result.Get<NumericMetric>(ArchitecturalRelevanceEvaluator.MetricName);

        Assert.True(metric.Value >= 0.8,
            $"Expected a well-formed ADR to score >= 0.8, got {metric.Value}. " +
            $"Reason: {metric.Interpretation?.Reason}");
    }

    // Calibration test #2 — an ADR deliberately missing "alternatives considered"
    // should score noticeably lower. This is the test that proves the judge is
    // actually checking the rubric, not just rubber-stamping everything.
    [Fact]
    public async Task AdrMissingAlternatives_ScoresLower()
    {
        await using ScenarioRun scenarioRun =
            await ReportingConfig.CreateScenarioRunAsync(nameof(AdrMissingAlternatives_ScoresLower));

        string adrText = await File.ReadAllTextAsync("TestData/adr-002-missing-alternatives.md");
        var messages = new[] { new ChatMessage(ChatRole.User, "Evaluate this ADR.") };
        var response = new ChatResponse(new ChatMessage(ChatRole.Assistant, adrText));

        EvaluationResult result = await scenarioRun.EvaluateAsync(messages, response);

        var metric = result.Get<NumericMetric>(ArchitecturalRelevanceEvaluator.MetricName);

        Assert.True(metric.Value < 0.8,
            $"Expected an ADR missing alternatives to score < 0.8, got {metric.Value}. " +
            $"Reason: {metric.Interpretation?.Reason}");
    }
}
