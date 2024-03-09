from django.shortcuts import render
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain_community.llms import HuggingFaceHub
import os

# huggingface Token
os.environ["HUGGINGFACEHUB_API_TOKEN"]='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'



@csrf_exempt
def post_function(request):
    if request.method == 'POST':
        try:
            # Get the URL from the JSON body of the request
            data = json.loads(request.body.decode('utf-8'))
            url=data['url']
            url_content=UnstructuredURLLoader([url]).load()


            llm = HuggingFaceHub(
                repo_id="mistralai/Mixtral-8x7B-Instruct-v0.1",
                task="text-generation",
                model_kwargs={
                    "max_new_tokens": 1032,
                    # "top_k": 30,
                    "temperature": 0.5,
                    "repetition_penalty": 1.03,
                },
            )
            chain = load_summarize_chain(llm, chain_type="stuff")
            result=chain.invoke(url_content)
            start=result['output_text'].find('CONCISE SUMMARY:')+16
            summary=result['output_text'][start:]

            

            
            # Return the modified URL in the response
            response_data = {'URL':url,'summary': summary}
            return JsonResponse(response_data, status=200)
        except Exception as e:
            # Handle exceptions as needed
            error_message = {'error occured in operation': str(e)}
            return JsonResponse(error_message, status=400)
    else:
        # Handle other HTTP methods if needed
        return JsonResponse({'error': 'Only POST requests allowed'}, status=405)

