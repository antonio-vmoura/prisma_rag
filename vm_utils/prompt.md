You will always receive **one single row of a CSV file**.
The CSV has the following columns:

```
"Document Title,Authors,Publication Year,Title: Skin,Abstract: Skin,First Removal,Abstract: Traditional ML,Second Removal,Duplication Status,Third Removal,Accepted or not,Proposed Model,Tasks (Objectives),Used Databases,Proposed Methodology,Evaluation Metrics and Results,Abstract,DOI,Author Keywords,Article Citation Count,PDF Link"
```

---

### Your task:

Using only the information contained in the row, analyze the article and answer the following questions.
Your output must be **strictly in CSV format** (no explanations, no additional text, no headers, no comments).

Questions (each one corresponds to a column in the output CSV, in the exact order):

```
"What model was proposed? (Expected Answer: Name/Architecture)","Is the model for skin lesion segmentation/classification? (Expected Answer: Yes / No)","Is it a new architecture or an adaptation? (Expected Answer: New / Adaptation)","Does it combine different methods (pre-processing + neural network + post-processing)? (Expected Answer: Yes / No)","Is the main objective segmentation or classification? (Expected Answer: Seg / Class)","Does the article perform feature extraction? (Expected Answer: Yes / No)","Does it work only with melanoma or with other types of skin cancer as well? (Expected Answer: Melanoma / Various)","What database was used (ISIC, PH2, HAM10000, etc.)? (Expected Answer: Dataset Name)","How many images were used? (Expected Answer: Nº images)","Is the dataset balanced between classes? (Expected Answer: Yes / No / Not informed)","Was there any image pre-processing? (Expected Answer: Yes / No)","How was the validation performed (train/test split or cross-validation)? (Expected Answer: Type of validation)","Does the article use transfer learning? (Expected Answer: Yes / No)","Were data augmentation techniques applied? Which ones? (Expected Answer: Ex: rotation, crop, flip)","Was it compared with state-of-the-art baselines? (Expected Answer: Yes / No)","What metrics were used (Dice, IoU, AUC, etc.)? (Expected Answer: List)","What was the best result achieved? (Expected Answer: Value)","Were the results compared with other state-of-the-art methods? (Expected Answer: Yes / No)","Was the model tested on different datasets (generalization)? (Expected Answer: Yes / No)","Does the article list limitations? Which ones? (Expected Answer: Short text)"
```

---

### Output format:

* Return only one CSV row with the answers, in the same order as the questions above.
* Do not repeat the input row.
* Do not include headers.
* Use commas `,` to separate fields.
* If some information is not present, write `Not informed`.