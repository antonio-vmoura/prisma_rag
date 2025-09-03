You will receive one single row of a CSV file with article metadata and abstract information.

Your task:
Analyze the row and answer the 20 questions below, using only the information in the row.

Important rules:
- Output must be ONLY one CSV row (no explanations, no headers, no comments, no extra text).
- Use commas to separate fields.
- Keep the answers in the exact same order as the questions.
- If the information is not present, write "Not informed".
- Never include the input row in the output.
- Never include extra text before or after the CSV.

Questions (each answer must match the expected format in parentheses):

1.  **What model was proposed?** (Name / Architecture)
2.  **Is the model for skin lesion segmentation/classification?** (Yes / No)
3.  **Is it a new architecture or an adaptation?** (New / Adaptation)
4.  **Does it combine different methods (pre-processing + neural network + post-processing)?** (Yes / No)
5.  **Is the main objective segmentation or classification?** (Segmentation / Classification)
6.  **Does the article perform feature extraction?** (Yes / No)
7.  **Does it work only with melanoma or with other types of skin cancer as well?** (Melanoma / Various)
8.  **What database was used (ISIC, PH2, HAM10000, etc.)?** (Dataset name)
9.  **How many images were used?** (Number of images)
10. **Is the dataset balanced between classes?** (Yes / No)
11. **Was there any image pre-processing?** (Yes / No)
12. **How was the validation performed (train/test split or cross-validation)?** (Validation type)
13. **Does the article use transfer learning?** (Yes / No)
14. **Were data augmentation techniques applied? Which ones?** (e.g., rotation, crop, flip)
15. **Was it compared with state-of-the-art baselines?** (Yes / No)
16. **What metrics were used (Dice, IoU, AUC, etc.)?** (List)
17. **What was the best result achieved?** (Value)
18. **Were the results compared with other state-of-the-art methods?** (Yes / No)
19. **Was the model tested on different datasets (generalization)?** (Yes / No)
20. **Does the article list limitations? Which ones?** (Short text)

Output format:
<answer1>,<answer2>,...,<answer20>