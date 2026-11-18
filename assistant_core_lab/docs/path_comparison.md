path                correct  abstain ok  p50 ms  max ms
deterministic          7/20       5/5     0.0     0.8   fails: E01 E02 E05 E06 E07 E08 E09 E10 E11 E12 E13 E14 E15
retrieval             16/20       4/5     0.1     0.2   fails: E13 E14 E15 E19
llm (stub)            16/20       4/5     0.3     8.4   fails: E13 E14 E15 E19

-We would use the retrieval path for handbook questions because it can find and answer many more questions using the official documents than the deterministic path.
-It is more suitable because it retrieves relevant paragraphs and provides answers based on the source documents, reducing the risk of making up information.
-The first failure we would fix is E13 ("when is tuition due") because the search fails to recognize the word "due" as matching the document's wording "paid by the end of week 6."
