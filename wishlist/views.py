from django.shortcuts import render

# Create your views here.
def addtowishList(request, wishlist):
    """_summary_

    Args:
        request (_type_): _description_
        wishlist (_type_): _description_

    Returns:
        _type_: _description_
    """
    wishlist = wishlist.objects.all()
    return render(request, 'wishlist/post_list.html')