using System.ClientModel;
using Arc42Toolkit.Evals.Evaluators;
using Microsoft.Extensions.AI;
using Microsoft.Extensions.AI.Evaluation;
using OpenAI;

namespace arc42Toolkit.Evaluations;

public class ArchitecturalRelevanceTests
{

    private static IChatClient CreateLmStudioClient() =>
        new OpenAIClient(
                new ApiKeyCredential("lm-studio"),
                new OpenAIClientOptions { Endpoint = new Uri("http://localhost:1234/v1") })
            .GetChatClient("microsoft/phi-4-reasoning-plus") 
            .AsIChatClient();

    // Calibration test #1 — a complete ADR should score well.
    // Use one of your real, well-formed ADRs here.
    [Fact]
    public async Task WellFormedAdr_ScoresHigh()
    {
        var chatClient = CreateLmStudioClient();
        var chatConfiguration = new ChatConfiguration(chatClient);
        var evaluator = new ArchitecturalRelevanceEvaluator();

        string adrText = await File.ReadAllTextAsync("TestData/adr-001-good.md");
        var messages = new[] { new ChatMessage(ChatRole.User, "Evaluate this ADR.") };
        var response = new ChatResponse(new ChatMessage(ChatRole.Assistant, adrText));

        EvaluationResult result = await evaluator.EvaluateAsync(
            messages, response, chatConfiguration, additionalContext: null, cancellationToken: default);

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
        var chatClient = CreateLmStudioClient();
        var chatConfiguration = new ChatConfiguration(chatClient);
        var evaluator = new ArchitecturalRelevanceEvaluator();

        string adrText = await File.ReadAllTextAsync("TestData/adr-002-missing-alternatives.md");
        var messages = new[] { new ChatMessage(ChatRole.User, "Evaluate this ADR.") };
        var response = new ChatResponse(new ChatMessage(ChatRole.Assistant, adrText));

        EvaluationResult result = await evaluator.EvaluateAsync(
            messages, response, chatConfiguration, additionalContext: null, cancellationToken: default);

        var metric = result.Get<NumericMetric>(ArchitecturalRelevanceEvaluator.MetricName);

        Assert.True(metric.Value < 0.8,
            $"Expected an ADR missing alternatives to score < 0.8, got {metric.Value}. " +
            $"Reason: {metric.Interpretation?.Reason}");
    }


}
