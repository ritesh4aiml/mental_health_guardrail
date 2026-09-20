
The proposed dual-model architecture combines a generative response model (Qwen2.5-1.5B-Instruct)
with an independent, class-weighted RoBERTa-based safety classifier, combined with a transparent
rule-based safety net into a four-tier escalation system (NONE/MODERATE/HIGH/CRITICAL). The
classifier was trained on the training split of MHDialog, its decision threshold was selected on the
validation split using a safety-first policy (maximize precision subject to recall >= 0.95),
and the full hybrid system was evaluated on the held-out test split.

The hybrid system achieved a precision of 0.649 (95% CI [0.486, 0.800]),
recall of 0.960 (95% CI [0.862, 1.000]), and F1-score of
0.774 (95% CI [0.632, 0.877]), against a majority-class baseline
accuracy of 0.610. The false-negative rate
was 0.040, which is the single most safety-critical number in this evaluation, since a missed
high-risk case has far more serious consequences than an unnecessary escalation. The selected policy
produced an escalation rate of 0.902 on the test set.

Every non-NONE assessment is written to a structured, hashed audit log, giving the system an explicit,
inspectable escalation trail rather than a silent decision. Qualitative before-and-after comparisons
showed that the guarded system preserves the standard generated response for NONE and MODERATE cases,
and replaces unrestricted generation with a safety-oriented response only when the input falls into a
selected content section (imminent_plan_or_method, self_harm_or_suicidal_ideation) or the model score
crosses the validation-selected HIGH threshold. Model-only CRITICAL escalation uses the stricter
threshold of 0.85, while explicit crisis-plan language remains a rule-based
CRITICAL override.

Limitations: the classifier's ground-truth labels are derived from the dataset's own risk-level
field (dataset_level source for the training split); the rule-based
component was deliberately kept out of label construction to avoid circular evaluation, but it is
still a small, manually curated keyword list and should not be assumed to generalize to phrasing not
represented in it. This remains a research prototype, not a clinically validated intervention, and
any real-world use requires clinical and ethical review.
