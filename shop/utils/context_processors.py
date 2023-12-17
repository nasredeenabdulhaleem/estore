# In a new file, for example myapp/context_processors.py
def global_context(request):
    context = {
        "global_variable": "Global Value",  # Replace this with your actual data
        # Add more key-value pairs as needed
    }
    return context
