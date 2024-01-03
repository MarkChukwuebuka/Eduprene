from django.shortcuts import render
import requests
from django.contrib import messages


# Create your views here.
def landing(request, *args, **kwargs):
    context = {

    }
    # https://learn.eduprene.com/landing?code=aeec60fc66
    api_endpoint = "https://eduprene-staging-7be6.onrender.com/api/v1/collector/email_collector/"
    referred_by = request.GET.get('code')
    if request.method == 'POST':
        first_name = request.POST.get('first-name')
        email = request.POST.get('email')

        data = {
                "email": email,
                "first_name": first_name,
                "referred_by": referred_by
            }

        try:
            # Send POST request
            response = requests.post(api_endpoint, data=data)

            # Check if the request was successful (status code 200)
            if response.status_code == 201:

                response_data = response.json()
                message = response_data['message']
                messages.success(request, f'{message}')
                return render(request, 'landing.html', context)

            elif response.status_code == 400:
                response_data = response.json()
                message = response_data['email'][0]
                messages.error(request, f'{message}')
                return render(request, 'landing.html', context)
                
                # return JsonResponse({'success': True, 'data': response_data})
            else:
                print(None)
                # return JsonResponse({'success': False, 'error': 'API request failed'})
        except requests.RequestException as e:
            return JsonResponse({'success': False, 'error': str(e)})

        


    return render(request, 'landing.html', context)










def post(self, request, *args, **kwargs):
        # Define the API endpoint URL
        

        # Your data to be sent in the POST request
        data = {
            'key1': 'value1',
            'key2': 'value2',
            # Add any other parameters as needed
        }

        try:
            # Send POST request
            response = requests.post(api_endpoint, data=data)

            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                # Parse the JSON response if applicable
                response_data = response.json()

                # Process the response data as needed
                # ...

                return JsonResponse({'success': True, 'data': response_data})
            else:
                return JsonResponse({'success': False, 'error': 'API request failed'})
        except requests.RequestException as e:
            return JsonResponse({'success': False, 'error': str(e)})