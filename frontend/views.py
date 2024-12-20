from django.shortcuts import render, redirect
import pandas as pd
import os
from django.http import HttpResponse, JsonResponse
from .models import CartItem
import json
from .data_processor import FashionDataProcessor
from .ai_assistant.fashion_assistant import (
    get_daily_outfit,
    get_outfit_approval,
    get_outfit_recommendations,
    load_and_prepare_data
)
from datetime import datetime

# Create your views here.
def shop(request):
    # Load the fashion dataset
    dataset_path = os.path.join('frontend', 'ai_assistant', 'fashion_dataset_full.pkl')
    df = pd.read_pickle(dataset_path)
    
    # Process the data for the template
    recommended_items = df.sample(n=15).to_dict('records')  # Random 4 items for recommended section
    trending_items = df.sample(n=15).to_dict('records')     # Random 4 items for trending section
    popular_items = df.sample(n=15).to_dict('records')      # Random 4 items for popular section
    
    context = {
        'recommended_items': recommended_items,
        'trending_items': trending_items,
        'popular_items': popular_items,
    }
    return render(request, 'shop.html', context)

def chat(request):
    return render(request, 'chat.html')

def process_chat_message(request):
    if request.method == 'POST':
        message = request.POST.get('message', '').lower()
        data = load_and_prepare_data()
        
        # Process different types of requests
        if 'outfit for the day' in message or 'what should i wear' in message:
            gender = 'Men' if 'men' in message else 'Women'
            outfit = get_daily_outfit(gender, data)
            return render(request, 'chat_response.html', {
                'user_message': request.POST.get('message'),
                'message': outfit['description'],
                'suggestions': outfit['items']
            })
            
        elif any(x in message for x in ['formal', 'casual']):
            gender = 'Men' if 'men' in message else 'Women'
            style = 'formal' if 'formal' in message else 'casual'
            recommendations = get_outfit_recommendations(f"{style} outfit", gender, data)
            return render(request, 'chat_response.html', {
                'user_message': request.POST.get('message'),
                'message': recommendations['description'],
                'suggestions': recommendations['items']
            })
            
        elif 'cart' in message and 'combination' in message:
            cart_items = CartItem.objects.all()
            items_data = [{'name': item.product_name, 'color': item.color} for item in cart_items]
            approval = get_outfit_approval(items_data)
            return render(request, 'chat_response.html', {
                'user_message': request.POST.get('message'),
                'message': approval['response'],
                'suggestions': []
            })
            
        else:
            # General fashion advice
            gender = 'Men' if 'men' in message else 'Women'
            recommendations = get_outfit_recommendations(message, gender, data)
            return render(request, 'chat_response.html', {
                'user_message': request.POST.get('message'),
                'message': recommendations['description'],
                'suggestions': recommendations['items']
            })
            
    return HttpResponse("Invalid request", status=400)

def add_to_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        size = request.POST.get('size')
        product_name = request.POST.get('product_name')
        price = request.POST.get('price')
        image_url = request.POST.get('image_url')
        
        # Check if item already exists
        cart_item, created = CartItem.objects.get_or_create(
            product_id=product_id,
            size=size,
            defaults={
                'product_name': product_name,
                'price': price,
                'image_url': image_url
            }
        )
        
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        
        # Return updated cart count
        cart_count = sum(item.quantity for item in CartItem.objects.all())
        if request.headers.get('HX-Request'):
            return HttpResponse(str(cart_count))
        return redirect('frontend:shop')
    
    return HttpResponse("Invalid request", status=400)

def update_quantity(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        action = request.POST.get('action')
        
        try:
            item = CartItem.objects.get(id=item_id)
            if action == 'increase':
                item.quantity += 1
            elif action == 'decrease':
                if item.quantity > 1:
                    item.quantity -= 1
                else:
                    item.delete()
                    if request.headers.get('HX-Request'):
                        return render(request, 'cart_items.html', get_cart_context())
                    return redirect('frontend:cart')
            item.save()
        except CartItem.DoesNotExist:
            return HttpResponse("Item not found", status=404)
        
        if request.headers.get('HX-Request'):
            return render(request, 'cart_items.html', get_cart_context())
        return redirect('frontend:cart')
    
    return HttpResponse("Invalid request", status=400)

def remove_from_cart(request, item_id):
    if request.method == 'POST':
        try:
            item = CartItem.objects.get(id=item_id)
            item.delete()
        except CartItem.DoesNotExist:
            pass
        
        if request.headers.get('HX-Request'):
            return render(request, 'cart_items.html', get_cart_context())
        return redirect('frontend:cart')
    
    return HttpResponse("Invalid request", status=400)

def get_cart_context():
    cart_items = CartItem.objects.all()
    total = sum(item.quantity * float(item.price) for item in cart_items)
    cart_count = sum(item.quantity for item in cart_items)
    return {'cart_items': cart_items, 'total': total, 'cart_count': cart_count}

def cart(request):
    context = get_cart_context()
    return render(request, 'cart.html', context)

def dashboard(request):
    data_processor = FashionDataProcessor()
    
    # Get statistics for dashboard
    category_stats = data_processor.get_category_stats()
    gender_dist = data_processor.get_gender_distribution()
    top_brands = data_processor.get_top_brands(5)
    season_dist = data_processor.get_season_distribution()
    
    # Convert data to JSON for JavaScript
    import json
    context = {
        'category_stats_labels': json.dumps(list(category_stats.keys())),
        'category_stats_values': json.dumps(list(category_stats.values())),
        'gender_dist_labels': json.dumps(list(gender_dist.keys())),
        'gender_dist_values': json.dumps(list(gender_dist.values())),
        'top_brands_labels': json.dumps(list(top_brands.keys())),
        'top_brands_values': json.dumps(list(top_brands.values())),
        'season_dist_labels': json.dumps(list(season_dist.keys())),
        'season_dist_values': json.dumps(list(season_dist.values())),
        'total_products': len(data_processor.df),
        'total_brands': len(data_processor.df['brand'].unique()),
    }
    return render(request, 'dashboard.html', context)

def analytics(request):
    """Handle analytics view with filtering"""
    data_processor = FashionDataProcessor()
    
    # Get filter parameters
    selected_category = request.GET.get('category', '')
    selected_gender = request.GET.get('gender', '')
    selected_season = request.GET.get('season', '')
    
    # Apply filters to get filtered dataset
    filters = {k: v for k, v in {
        'masterCategory': selected_category,
        'gender': selected_gender,
        'season': selected_season
    }.items() if v}  # Only include non-empty filters
    
    filtered_df = data_processor.get_products_by_filters(filters)
    
    # Calculate statistics
    total_products = len(filtered_df)
    total_categories = filtered_df['masterCategory'].nunique()
    total_colors = filtered_df['baseColour'].nunique()
    
    # Prepare chart data
    yearly_trends = filtered_df.groupby('year').size()
    color_dist = filtered_df['baseColour'].value_counts().nlargest(10)
    category_stats = filtered_df['masterCategory'].value_counts().nlargest(10)
    gender_dist = filtered_df['gender'].value_counts()
    
    # Convert data to JSON-safe format
    context = {
        'total_products': total_products,
        'total_categories': total_categories,
        'total_colors': total_colors,
        'yearly_trends_labels': yearly_trends.index.tolist(),
        'yearly_trends_values': yearly_trends.values.tolist(),
        'color_dist_labels': color_dist.index.tolist(),
        'color_dist_values': color_dist.values.tolist(),
        'category_stats_labels': category_stats.index.tolist(),
        'category_stats_values': category_stats.values.tolist(),
        'gender_dist_labels': gender_dist.index.tolist(),
        'gender_dist_values': gender_dist.values.tolist(),
        'filter_options': data_processor.get_filter_options(),
        'selected_category': selected_category,
        'selected_gender': selected_gender,
        'selected_season': selected_season
    }
    
    # If it's an HTMX request, return only the charts
    if request.headers.get('HX-Request'):
        return render(request, 'analytics_charts.html', context)
    
    return render(request, 'analytics.html', context)

def products(request):
    """Handle products view with filtering and pagination"""
    data_processor = FashionDataProcessor()
    
    # Get filter parameters from request
    category = request.GET.get('category', '')
    gender = request.GET.get('gender', '')
    color = request.GET.get('color', '')
    season = request.GET.get('season', '')
    brand = request.GET.get('brand', '')
    page = int(request.GET.get('page', 1))
    per_page = 20  # Limit products per page
    
    # Apply filters
    filtered_df = data_processor.get_products_by_filters({
        'masterCategory': category,
        'gender': gender,
        'baseColour': color,
        'season': season,
        'brand': brand
    })
    
    # Calculate pagination
    total_products = len(filtered_df)
    total_pages = (total_products + per_page - 1) // per_page
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    
    # Get paginated products
    paginated_products = filtered_df.iloc[start_idx:end_idx].to_dict('records')
    
    # Get filter options for dropdowns
    filter_options = data_processor.get_filter_options()
    
    context = {
        'products': paginated_products,
        'filter_options': filter_options,
        'current_page': page,
        'total_pages': total_pages,
        'total_products': total_products,
        'has_next': page < total_pages,
        'has_prev': page > 1,
        'next_page': page + 1,
        'prev_page': page - 1,
        'current_filters': {
            'category': category,
            'gender': gender,
            'color': color,
            'season': season,
            'brand': brand
        }
    }
    
    # If it's an HTMX request, return only the products grid
    if request.headers.get('HX-Request'):
        return render(request, 'products_grid.html', context)
    
    return render(request, 'products.html', context)