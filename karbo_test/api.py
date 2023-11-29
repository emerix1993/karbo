from django.http import JsonResponse
from django.views import View
import requests
from .config import API_KEY
from .serializers import NewsSerializer


class ViewForApi(View):
    def get(self, request):
        api_key = API_KEY
        if api_key is None:
            return JsonResponse({"error": "API_KEY not found in environment variables"}, status=500)

        url = f"https://cryptopanic.com/api/v1/posts/?auth_token={api_key}"

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            print("Received data:", data)

            if 'results' in data:
                for post_data in data['results']:
                    if all(key in post_data for key in
                           ['kind', 'domain', 'source', 'title', 'published_at', 'slug', 'id', 'url', 'created_at',
                            'votes']):
                        serializer = NewsSerializer(data=post_data)
                        if serializer.is_valid():
                            serializer.save()
                            print("Data added to the database successfully")
                        else:
                            print("Serializer errors:", serializer.errors)
                    else:
                        print("Some required fields are missing for this post. Skipping.")

                return JsonResponse({"message": "Data added to the database successfully"})
            else:
                return JsonResponse({"error": "No 'results' field in the API response"}, status=500)

        except requests.RequestException as e:
            return JsonResponse({"error": f"Error: {str(e)}"}, status=500)
