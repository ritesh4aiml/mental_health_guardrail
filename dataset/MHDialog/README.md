---
language:
- en
license: cc-by-nc-sa-4.0
size_categories:
- 1K<n<10K
task_categories:
- text-classification
task_ids:
- multi-class-classification
- multi-label-classification
pretty_name: MHDialog Mental Health AI Dialogue Dataset
tags:
- mental-health
- dialogue
- multi-task
- risk-assessment
- suicide-prevention
- nlp
dataset_info:
  features:
  - name: Dialogue
    dtype: string
  - name: Dialog Intent
    dtype: string
  - name: Concern Type
    dtype: string
  - name: Level
    dtype: string
  splits:
  - name: train
    num_examples: 700
  - name: validation
    num_examples: 150
  - name: test
    num_examples: 150
configs:
- config_name: default
  data_files:
  - split: train
    path: train.csv
  - split: validation
    path: val.csv
  - split: test
    path: test.csv
---

# MHDialog: Mental Health AI Dialogue Dataset

## Dataset Description

- **Homepage:** [Project Dashboard](https://mhdash.socialshields.org/)
- **Paper:** [MHDash: An Online Platform for Benchmarking Mental Health-Aware AI Assistants](https://arxiv.org/abs/2602.00353)
- **Point of Contact:** [yihe.zhang@louisiana.edu](mailto:yihe.zhang@louisiana.edu)

### Dataset Summary

MHDialog is a multi-turn dialogue dataset for mental health support conversation analysis. It contains 1,000 dialogues with multi-dimensional annotations covering dialog intent (8 categories), concern type (7 categories), and risk level (6 levels).

The dataset is designed for multi-task classification research in mental health NLP, enabling the development of models that can simultaneously assess conversational strategies, identify mental health concerns, and evaluate risk severity.

### Supported Tasks

- **Multi-task Text Classification**: Jointly predicting dialog intent, concern type, and risk level
- **Risk Assessment**: Identifying high-risk mental health situations
- **Dialogue Understanding**: Analyzing patterns in mental health support conversations

### Languages

English (en)

## Dataset Structure

### Data Instances

```json
{
  "Dialogue": "[{\"round\": 1, \"user\": \"I don't know if I can keep going...\", \"supporter\": \"I'm here to listen...\"}, ...]",
  "Dialog Intent": "Recovery",
  "Concern Type": "Behavior", 
  "Level": "Moderate"
}
```

### Data Fields

| Field | Type | Description |
|-------|------|-------------|
| `Dialogue` | string | JSON-formatted 10-round dialogue between user and supporter |
| `Dialog Intent` | string | One of 8 dialogue strategy categories |
| `Concern Type` | string | One of 7 mental health concern categories |
| `Level` | string | One of 6 risk severity levels |

### Data Splits

| Split | Examples |
|-------|----------|
| train | 700 |
| validation | 150 |
| test | 150 |

## Label Definitions

### Dialog Intent (8 categories)
- **Recovery**: User shows signs of improvement or willingness to seek help
- **Adversarial**: User resists support or shows hostility
- **Crisis Escalation**: Situation intensifies during conversation
- **Avoidance**: User avoids engaging with the support or topic
- **Explicit Help-seeking**: User directly asks for help or resources
- **Emotional Venting**: User expresses emotions without seeking solutions
- **Implicit Help-seeking**: User indirectly signals a need for support
- **Validation-Seeking**: User seeks acknowledgment or affirmation

### Concern Type (7 categories)
- **Behavior**: Self-harm behaviors or concerning actions
- **Ideation**: Suicidal thoughts or ideation
- **Attempt**: History or current suicide attempts
- **Indicator**: Warning signs or risk indicators
- **Supportive**: Seeking support for others
- **Not Related**: Content not related to mental health concerns
- **Unsure**: Cannot be determined

### Risk Level (6 levels)
- **No**: No apparent risk indicators
- **Minor**: Minimal risk indicators
- **Moderate**: Some concerning elements present
- **Not Related**: Content not related to mental health risk
- **Severe**: Immediate concern warranted
- **Unsure**: Risk level cannot be determined

## Dataset Creation

### Curation Rationale

This dataset was created to address the need for multi-dimensional analysis of mental health support conversations. Existing datasets often focus on single classification tasks, while real-world mental health assessment requires understanding multiple aspects simultaneously.

### Source Data

#### Initial Data Collection
- Original posts sourced from public Reddit mental health communities
- Posts selected to represent diverse mental health concerns and risk levels

#### Dialogue Generation
- 10-round dialogues generated using large language models
- Dialogues simulate supportive conversations between users and peer supporters

### Annotations

#### Annotation Process
- Labels assigned by trained annotators
- Multi-dimensional annotation covering intent, concern type, and risk level

#### Who are the annotators?
Trained annotators with background in mental health support

## Considerations for Using the Data

### Social Impact

This dataset aims to advance mental health NLP research and improve automated support systems. Proper use can help:
- Develop better mental health chatbots
- Train risk assessment models
- Understand patterns in support conversations

### Discussion of Biases

- Dataset reflects patterns in Reddit mental health communities
- Synthetic dialogues may not capture all real-world conversation dynamics
- Annotation reflects annotator judgment and training

### Other Known Limitations

- English only
- Synthetic dialogues (not real conversations)
- Limited to text-based interactions

## Additional Information

### Dataset Curators

Yihe Zhang

University of Louisiana at Lafayette

### Licensing Information

CC BY-NC-SA 4.0 (Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International)

### Citation Information

```bibtex
@misc{zhang2026mhdashonlineplatformbenchmarking,
      title={MHDash: An Online Platform for Benchmarking Mental Health-Aware AI Assistants}, 
      author={Yihe Zhang and Cheyenne N Mohawk and Kaiying Han and Vijay Srinivas Tida and Manyu Li and Xiali Hei},
      year={2026},
      eprint={2602.00353},
      archivePrefix={arXiv},
      primaryClass={cs.AI},
      url={https://arxiv.org/abs/2602.00353}, 
}
```



### Contributions

Thanks to all contributors who helped create this dataset.
