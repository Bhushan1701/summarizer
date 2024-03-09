from django.shortcuts import render
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain_community.llms import HuggingFaceHub
import os

# setting huggingface Token
os.environ["HUGGINGFACEHUB_API_TOKEN"]='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'



# creating post method and excempting csrf to not give certificate error
@csrf_exempt
def post_function(request):
    if request.method == 'POST':
        try:
           
            try:
                # fetching url and scrapping data using unstructured loader
                data = json.loads(request.body.decode('utf-8'))
                url=data['url']
                url_content=UnstructuredURLLoader([url]).load()
            except Exception as e:
                error_message = {'error occured in fetching the url data': str(e)}
                return JsonResponse(error_message)

            try :
                # setting up mixtral llm from huggingface
                llm = HuggingFaceHub(
                    repo_id="mistralai/Mixtral-8x7B-Instruct-v0.1",
                    task="text-generation",
                    model_kwargs={
                        "temperature": 0.1,
                        "repetition_penalty": 1.03,
                    },
                )

                # creating summarize chain from langchain
                chain = load_summarize_chain(llm, chain_type="stuff")
                result=chain.invoke(url_content)
                # slicing the llm summary output
                start=result['output_text'].find('CONCISE SUMMARY:')+15
                summary=result['output_text'][start:-1]
            except Exception as e:
                error_message = {'error occured in getting the summary from LLM ': str(e)}
                return JsonResponse(error_message)


            
            # Return the summary and url in response
            response_data = {'URL':url,'summary': summary}
            return JsonResponse(response_data, status=200)
        except Exception as e:
            # Handle exceptions as needed
            error_message = {'error occured in operation': str(e)}
            return JsonResponse(error_message, status=400)
    else:
        # Handle other HTTP methods if needed
        return JsonResponse({'error': 'Only POST requests allowed'}, status=405)

