# REQUIRED SEEDERS

- Color requires an instance with `Default` as the value for both the `name` and `color`.

- Size requires an instance with `Default` as the value for both the `title` and `size`.

- Variation requires instances with:
  - `Default` as the value for the `name`.
  - `Size` as the value for the `name`.
  - `Size` and `Color` as the value for the `name`.


<!-- """

# I want to create a class that will handle all the requests to the monnify api
#  it would be a class that will have all the methods that will be used to make the requests
# it should instantiate the requests session and use it to make the requests
# also it should be able to handle the response and return the response in a json format
# it should be able to set the standard time for each request putting security in mind
# it should be able to handle errors and return the error in a json format
#  the class should follow global best practices dry and kiss principles
# pep8 and pep257 should be followed with black and flake8
# security should be put in mind because it is a payment gateway api integration package

# i want to be able to be able to check the environment where the package is being used and get the user credentials from the environment variables using Constatnts MONNIFY_API_KEY, MONNIFY_SECRET_KEY, MONNIFY_BASE_URL, MONNIFY_ENVIRONMENT
# also i want to be able to check if the user has passed the credentials as arguments to the class and use them instead of the environment variables
"""
# def get_access_token(self):
#         url = self.base_url + "/api/v1/auth/login"
#         payload = {"AUTHORIZATION": self.AUTHORIZATION}
#         try:
#             response = requests.post(
#                 url, headers=self.headers, data=json.dumps(payload)
#             )
#         except Exception as e:
#             data = {"success": False, "error": str(e)}
#             # error_email({'error':str(e)})
#         # print(response.json())
#         return response.json()["responseBody"]["accessToken"]

# the commented out def get_access_token(self) is a method that i want to use to get the access token from the monnify api it response wich a json object that has the access token in it will be used as a bearer authorization for any other request to the api
# How do i effectively intergrate this method into the class and make it work for all the methods in the class and also note that the header that will be used would be in this format         
headers = {
            "Authorization": "Bearer " + self.get_access_token(),
            "Content-Type": "application/json",
        }
# How do i make the headers to be used in all the methods in the class
# also the access token has an expiry time how do i take note of expiry time and request for a new token without braking the system
""" -->
