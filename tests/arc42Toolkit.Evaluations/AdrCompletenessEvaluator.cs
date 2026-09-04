using System.Text.RegularExpressions;
using Microsoft.Extensions.AI;
using Microsoft.Extensions.AI.Evaluation;

namespace arc42Toolkit.Evaluations.Evaluators;

/// <summary>
/// An LLM-as-judge IEvaluator that scores an Architecture Decision Record (ADR),
/// written using Michael Nygard's template (Title, Status, Context, Decision,
/// Consequences), against a fixed rubric: context, decision, consequences, and
/// alternatives considered.
/// </summary>
public sealed class AdrCompletenessEvaluator : IEvaluator
{
    public const string MetricName = "AdrCompleteness";

    public IReadOnlyCollection<string> EvaluationMetricNames => [MetricName];

    public async ValueTask<EvaluationResult> EvaluateAsync(
        IEnumerable<ChatMessage> messages, 
        ChatResponse modelResponse, 
        ChatConfiguration? chatConfiguration, 
        IEnumerable<EvaluationContext>? additionalContext, 
        CancellationToken cancellationToken)
    {
        if (chatConfiguration?.ChatClient is null)
        {
            throw new InvalidOperationException(
                $"{nameof(AdrCompletenessEvaluator)} requires a {nameof(ChatConfiguration)} " +
                "with a valid ChatClient to act as the judge.");
        }

        string adrText = modelResponse.Text ?? string.Empty;

        if (string.IsNullOrWhiteSpace(adrText))
        {
            var emptyMetric = new NumericMetric(MetricName, 0.0);
            emptyMetric.AddDiagnostics(
                EvaluationDiagnostic.Error("The ADR text was empty; nothing to evaluate."));
            return new EvaluationResult(emptyMetric);
        }

        string judgePrompt = $"""
            You are reviewing an Architecture Decision Record (ADR) written for a software project.
            The ADR follows Michael Nygard's template: Title, Status, Context, Decision, and
            Consequences. There is no dedicated "Alternatives" heading in this template — when
            alternatives are discussed, they will typically appear as prose inside the Context
            section (options that were weighed) or the Consequences section (why the rejected
            options were not chosen). Do not penalize the ADR for lacking a separate alternatives
            heading; look for the content wherever it appears.

            Score how well it satisfies the following four criteria, each worth 0.25 points:

            1. CONTEXT — states the problem or forces that motivated the decision
            2. DECISION — states a clear, unambiguous decision that was made
            3. CONSEQUENCES — documents resulting consequences, both positive and negative
            4. ALTERNATIVES — mentions at least one alternative that was considered and why it was rejected

            ADR TEXT:
            ---
            {adrText}
            ---

            Respond in EXACTLY this format, nothing else:
            SCORE: <a number between 0.0 and 1.0>
            REASON: <one sentence explaining what is present and what, if anything, is missing>
            """;

        var judgeMessages = new List<ChatMessage>
        {
            new(ChatRole.User, judgePrompt)
        };

        // Reasoning-model judges occasionally drift from the requested format on the
        // first attempt (e.g. leaking chain-of-thought before the SCORE line). Give the
        // judge one chance to correct itself before treating it as a real failure.
        const int maxAttempts = 2;
        double score = 0.0;
        string reason = string.Empty;
        string lastJudgeText = string.Empty;
        bool parsed = false;

        for (int attempt = 1; attempt <= maxAttempts; attempt++)
        {
            ChatResponse judgeResponse = await chatConfiguration.ChatClient
                .GetResponseAsync(judgeMessages, cancellationToken: cancellationToken)
                .ConfigureAwait(false);

            lastJudgeText = judgeResponse.Text ?? string.Empty;
            parsed = TryParseJudgeResponse(lastJudgeText, out score, out reason);

            if (parsed)
            {
                break;
            }

            if (attempt < maxAttempts)
            {
                judgeMessages.Add(new ChatMessage(ChatRole.Assistant, lastJudgeText));
                judgeMessages.Add(new ChatMessage(ChatRole.User, """
                    Your previous reply did not contain a line starting with "SCORE:" followed by a
                    number. Reply again using EXACTLY this format, nothing else:
                    SCORE: <a number between 0.0 and 1.0>
                    REASON: <one sentence explaining what is present and what, if anything, is missing>
                    """));
            }
        }

        if (!parsed)
        {
            // Fail loud rather than silently returning 0 — a parsing failure after a
            // retry is a bug in the prompt or the judge model, not a legitimate "bad
            // ADR" verdict.
            throw new FormatException(
                $"Could not parse a SCORE from the judge response after {maxAttempts} attempts. " +
                $"Last raw response:\n{lastJudgeText}");
        }

        var metric = new NumericMetric(MetricName, score);
        metric.Interpretation = new EvaluationMetricInterpretation(
            rating: score >= 0.8 ? EvaluationRating.Good
                  : score >= 0.5 ? EvaluationRating.Average
                  : EvaluationRating.Poor,
            reason: reason);

        // Keep the raw judge output attached for debugging when a score looks wrong.
        metric.AddDiagnostics(EvaluationDiagnostic.Informational(lastJudgeText));

        return new EvaluationResult(metric);
    }

    private static bool TryParseJudgeResponse(string judgeText, out double score, out string reason)
    {
        // Deliberately tolerant regex parsing — real model output has minor formatting drift
        // (extra whitespace, markdown bold, etc.) even when told to follow a fixed format.
        var scoreMatch = Regex.Match(judgeText, @"SCORE:\s*([0-9]*\.?[0-9]+)", RegexOptions.IgnoreCase);
        var reasonMatch = Regex.Match(judgeText, @"REASON:\s*(.+)", RegexOptions.IgnoreCase | RegexOptions.Singleline);

        if (!scoreMatch.Success || !double.TryParse(scoreMatch.Groups[1].Value, out score))
        {
            score = 0.0;
            reason = string.Empty;
            return false;
        }

        score = Math.Clamp(score, 0.0, 1.0);
        reason = reasonMatch.Success
            ? reasonMatch.Groups[1].Value.Trim()
            : "(no reason provided by judge)";

        return true;
    }
}