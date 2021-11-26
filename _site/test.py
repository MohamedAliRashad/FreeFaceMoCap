
def get_metrics(data, pprint=False):
    
    template = "{:.2%}"
    
    true_positives = data["true_positives"] # gt == indomain class x == prediction
    true_negatives = data["true_negatives"] # gt == out of domain == prediction
    false_negatives = data["false_negatives"] # gt == in domain class x, prediction == out of domain
    false_positives = data["false_positives"] # gt == out of domain , prediction == in domain class x
    misclassified = data["misclassified"] # gt == in domain class x, prediction == in domain class y
    
    num_indomain_samples = true_positives + false_negatives + misclassified
    num_outdomain_samples = true_negatives + false_positives
    total_num_samples = num_indomain_samples + num_outdomain_samples
    
    # First step evaluation (cross_domain)
    Specificity = true_negatives / num_outdomain_samples
    
    # Second step evaluation (indomain)
    # Precision = true_positives / (true_positives + false_positives + misclassified)
    Recall = true_positives / num_indomain_samples
    inter_class_specificity = true_positives / (true_positives + misclassified)
    
    stats = {"total_num_samples": total_num_samples,
    "num_indomain_samples": num_indomain_samples,
    "num_outdomain_samples": num_outdomain_samples
    }
    if pprint:
        Specificity = template.format(Specificity)
        inter_class_specificity = template.format(inter_class_specificity)
        Recall = template.format(Recall)
        
        result = {
        "normalized_tp": template.format(true_positives / total_num_samples),
        "normalized_tn": template.format(true_negatives / total_num_samples),
        "normalized_fn": template.format(false_negatives / total_num_samples),
        "normalized_fp": template.format(false_positives / total_num_samples),
        "normalized_miss": template.format(misclassified / total_num_samples),
        "summary_metrics": {"outdomain_specificity": Specificity, "indomain_precision": inter_class_specificity, "indomain_recall": Recall}
        }
        
    else:
        result = {
        "normalized_tp": true_positives / total_num_samples,
        "normalized_tn": true_negatives / total_num_samples,
        "normalized_fn": false_negatives / total_num_samples,
        "normalized_fp": false_positives / total_num_samples,
        "normalized_miss": misclassified / total_num_samples,
        "summary_metrics": {"outdomain_specificity": Specificity, "indomain_precision": inter_class_specificity, "indomain_recall": Recall}
        }
    output = {**stats, **result}
    
    
    return output


import json

data = """   

"true_positives": 250, 

"true_negatives": 134, 

"false_negatives": 4, 

"false_positives": 401, 

"misclassified": 63 
"""
x = data.strip().split("\n")
x = [i for i in x if i != '']
x = [i.strip().replace(",", "").split(" ") for i in x]
x = {i[0].replace(":","").replace('"',''):int(i[1]) for i in x}
print(x)
print(json.dumps(get_metrics(x, pprint=True)["summary_metrics"], indent=4))
[print(z) for z in list(get_metrics(x, pprint=True)["summary_metrics"].values())]