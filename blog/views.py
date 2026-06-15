from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from .models import Post
from .forms import PostForm
from django.contrib.auth.decorators import login_required






def home(request):
    posts = Post.objects.all() 

    context = {
        'posts': posts
    }
    return render(request, 'blog/home.html', context)

def about(request):
    return render(request ,'blog/about.html')


def ad_test_lab(request):
    campaigns = [
        {
            "name": "Search launch promo",
            "source": "google",
            "medium": "cpc",
            "campaign": "spring_launch_test",
            "channel": "Paid Search",
            "landing_path": "writing-kit",
            "click_id": "gclid",
            "click_value": "TEST-GCLID-SEARCH-001",
            "campaign_id": "cmp_search_001",
            "creative_id": "crt_text_ad_001",
            "placement_id": "plc_google_top_001",
        },
        {
            "name": "Social carousel promo",
            "source": "facebook",
            "medium": "paid_social",
            "campaign": "reader_growth_test",
            "channel": "Paid Social",
            "landing_path": "membership",
            "click_id": "fbclid",
            "click_value": "TEST-FBCLID-SOCIAL-002",
            "campaign_id": "cmp_social_002",
            "creative_id": "crt_carousel_002",
            "placement_id": "plc_feed_mobile_002",
        },
        {
            "name": "Newsletter retargeting",
            "source": "bing",
            "medium": "cpc",
            "campaign": "newsletter_retargeting_test",
            "channel": "Microsoft Ads",
            "landing_path": "newsletter",
            "click_id": "msclkid",
            "click_value": "TEST-MSCLKID-BING-003",
            "campaign_id": "cmp_bing_003",
            "creative_id": "crt_newsletter_003",
            "placement_id": "plc_sidebar_003",
        },
    ]

    for campaign in campaigns:
        query_string = (
            f"utm_source={campaign['source']}"
            f"&utm_medium={campaign['medium']}"
            f"&utm_campaign={campaign['campaign']}"
            f"&campaign_id={campaign['campaign_id']}"
            f"&creative_id={campaign['creative_id']}"
            f"&placement_id={campaign['placement_id']}"
            f"&{campaign['click_id']}={campaign['click_value']}"
        )
        campaign["landing_url"] = f"/offers/{campaign['landing_path']}/?{query_string}"

    return render(request, "blog/ad_test_lab.html", {"campaigns": campaigns})


def ad_landing_page(request, offer_slug):
    offers = {
        "writing-kit": {
            "title": "The Field Notes Writing Kit",
            "headline": "A focused kit for sharper drafts.",
            "body": "A placeholder product page built to test paid search attribution and page metadata capture.",
            "cta": "Start Drafting",
            "tag": "Writing Tools",
        },
        "membership": {
            "title": "Inkwell Reader Membership",
            "headline": "Support independent essays and deep reads.",
            "body": "A placeholder membership landing page for paid social traffic and campaign testing.",
            "cta": "Join the Circle",
            "tag": "Membership",
        },
        "newsletter": {
            "title": "The Sunday Letter",
            "headline": "A weekly note for curious readers.",
            "body": "A placeholder newsletter page for retargeting tests from Microsoft Ads and sidebar placements.",
            "cta": "Subscribe Free",
            "tag": "Newsletter",
        },
    }
    offer = offers.get(offer_slug, offers["writing-kit"])

    return render(
        request,
        "blog/ad_landing_page.html",
        {
            "offer": offer,
            "offer_slug": offer_slug,
            "query_items": request.GET.items(),
        },
    )



@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  
            post.save()
            return redirect('home')
    else:
        form = PostForm()

    return render(request, 'blog/create_post.html', {'form': form})
@login_required
def profile(request):
    posts = Post.objects.filter(author=request.user) 

    context = {
        'posts': posts
    }
    return render(request, 'blog/profile.html', context)


@login_required
def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if post.author != request.user:
        return redirect('home')

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post) 
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = PostForm(instance=post) 

    return render(request, 'blog/edit_post.html', {'form': form})


@login_required

def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if post.author != request.user:
        return redirect('home')

    if request.method == 'POST':
        post.delete()
        return redirect('profile')

    return render(request, 'blog/delete_post.html', {'post': post})




# Create your views here.
