import requests
from django.http import JsonResponse

def get_gene_data(request, gene_name):
    # Ensembl API to get gene data by symbol
    url = f"https://rest.ensembl.org/lookup/symbol/human/{gene_name}?content-type=application/json"
    response = requests.get(url)

    # Debug: Print the status code and response to the console
    print("Status Code:", response.status_code)
    print("Response Body:", response.text)

    if response.status_code == 200:
        data = response.json()
        gene_info = {
            "gene_name": data.get("display_name"),
            "description": data.get("description"),
            "chromosome": data.get("seq_region_name"),
            "start": data.get("start"),
            "end": data.get("end"),
            "strand": data.get("strand"),
            "external_ids": data.get("external_ids", []),
        }

        # Fetch related drugs (if any)
        drugs_url = f"https://rest.ensembl.org/overlap/id/{data['id']}?feature=variation;content-type=application/json"
        drugs_response = requests.get(drugs_url)
        if drugs_response.status_code == 200:
            drugs_data = drugs_response.json()
            gene_info["related_drugs"] = [drug.get('drug_name') for drug in drugs_data if 'drug_name' in drug]
        else:
            gene_info["related_drugs"] = []

        return JsonResponse(gene_info)

    return JsonResponse({"error": "Gene not found"}, status=404)
