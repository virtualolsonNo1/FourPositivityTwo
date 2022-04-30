from django import template

register = template.Library()
@register.filter
def get_item(dictionary, key):
    buyers = dictionary.get(key)
    if buyers is None:
        return ""
    
    response = "Recently purchased by " + buyers[0]
    for user in range(1,len(buyers)):
        response = response + ", " + buyers[user]
    return response