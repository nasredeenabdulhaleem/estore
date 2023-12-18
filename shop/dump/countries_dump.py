import requests
from shop.models import Country  # Replace with your actual Country model import

def dump_countries():
    response = requests.get('https://restcountries.com/v2/all')
    data = response.json()

    for country_data in data:
        country, created = Country.objects.get_or_create(
            country_name=country_data['name'],
            defaults={
                # Add any other fields you want to populate here
            }
        )

        if created:
            print(f'Added {country.country_name} to the database.')
        else:
            print(f'{country.country_name} already exists in the database.')

# Call the function to start the data dump
# dump_countries()
"""
{% if address %}
            <div class="py-4">
                <h2 class="text-xl font-semibold mb-4">Shipping Information</h2>
                <div class="space-y-2">
                    <p class="text-accent-content"><span class="text-gray-500">Name: </span>{{data.user.fullname}}</p>
                    <p class="text-accent-content"><span class="text-gray-500">Adress:
                        </span>{{address.address.full_address}}</p>
                    <p class="text-accent-content"><span class="text-gray-500">City: </span>{{address.address.city}}</p>
                    <div class="flex space-x-2">
                        <p class="text-accent-content"><span class="text-gray-500">Location:
                            </span>{{address.address.state}}, {{address.address.country}}</p>
                        <p class="text-accent-content"><span class="text-gray-500">Postal Code:
                            </span>{{address.address.postal_code}}</p>
                    </div>
                </div>
            </div>
            {% else %}
            <div class="py-4">
                <h2 class="text-xl font-semibold mb-4">Shipping Information</h2>
                <div class="space-y-2">
                    <input type="text" class="input input-bordered" placeholder="Full Name">
                    <input type="text" class="input input-bordered" placeholder="Shipping Address">
                    <input type="text" class="input input-bordered" placeholder="City">
                    <div class="flex space-x-2">
                        <input type="text" class="input input-bordered" placeholder="State">
                        <input type="text" class="input input-bordered" placeholder="Zip Code">
                    </div>
                </div>
            </div>
            {% endif %}
"""