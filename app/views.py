from django.shortcuts import render, redirect
from navbar.forms import ContactForm
from django.views import View
from django.shortcuts import get_object_or_404
from django.contrib import messages
from document.models import Article, ArticleImage, ArticleCategory
from navbar.models import Contact
from django.urls import reverse
import datetime
import  subprocess
from app import bot

# Create your views here.
def index(request):
    objs = Article.objects.filter(category=1)
    return render(request, 'index.html', context={'articles' : objs})

class IndexView(View):
    def get(self, request):
        category_id = ArticleCategory.objects.get(name="Yangiliklar")
        articles = Article.objects.filter(category=category_id).order_by('-id')
        article = articles[0]

        articles = articles[0:4]

        context = {
                'articles':articles,
                'article':article,
                }
        return render(request, 'index.html', context)
        
        
class CategoryView(View):
    
    def get(self, request, id):
        # articles = get_object_or_404(Article, category = id)
        articles = Article.objects.filter(category = id).order_by('-id')
        article = ArticleCategory.objects.get(id=id)
        # print("=============================================", article)
        
        if str(article) == "Bog'lanish":
            form = ContactForm()
            return render(request, "contact.html", {'form':form})
        
        elif str(article) in ["Yangiliklar"]:
            # print("--------------------------------------", request)
            context = {
                '_id':id,
                'articles':articles,
                'article':article,
                }
            return render(request, 'article_list.html', context)
        
        
        elif str(article) in ["Qonunlar", "Qarorlar", "Farmonlar", "Standartlar", "Dasturlar", "Loyihalar", "E'lonlar"]:
            # print("--------------------------------------", request)
            context = {
                '_id':id,
                'articles':articles,
                'article':article,
                }
            return render(request, 'documents_list.html', context)
        

        else:
            if articles:
                context = {
                    '_id':id,
                    'article':articles[0],
                    }
                return render(request, 'one_page_detail.html', context)
            else:
                category_id = ArticleCategory.objects.get(name="Yangiliklar")
                articles = Article.objects.filter(category=category_id)
                article = Article.objects.filter(category=category_id)[len(articles)-1]

                articles = articles[0:4]

                context = {
                        'articles':articles,
                        'article':article,
                        }
                return render(request, 'index.html', context)
            
            
                
    def post(self, request, id):
        # article = ArticleCategory.objects.get(id=id)
    
        # form = ContactForm(data=request.POST)
        data = request.POST.dict()
        name = data.get("first_name")
        phone = data.get("phone")
        body = data.get("body")
  
            
        today = datetime.date.today()
        formatted_date = today.strftime("%Y-%m-%d")
       

        text = f"""
📝 Yangi xabar:\n
🙍🏻‍♂️ Fuqaro: {name}
📲 Telefon: {phone}
📩 Xabar: {body}
📅 Sana: {formatted_date}
"""
        with open('app/data.txt', 'w') as file:
            file.write(str(text))

            
        try:
            bot.run_bot()
            
            # subprocess.run(['python', 'app/bot.py'])
            
        except Exception as e:
            print(f"============================ Error executing the script: {e}")

        

        category_id = ArticleCategory.objects.get(name="Yangiliklar")
        articles = Article.objects.filter(category=category_id).order_by('-id')
        article = articles[0]

        articles = articles[0:4]

        context = {
                'articles':articles,
                'article':article,
                }
      
        return redirect("app:index")
        
        # return render(request, "article_list.html", context)
    
    
    
    
    
class CategoryDetailView(View):
    def get(self, request,category_id, id):
        # articles = get_object_or_404(Article, category = id)
        article = Article.objects.get(id=id)
        articles = Article.objects.filter(category=category_id).order_by('-id')
        article.views += 1  # Ko'rishlar sonini 1 ga oshirish
        article.save()
      
        context = {
            'category_id':category_id,
            'article':article,
            'articles':articles[0:10],
            }
        # print("==========================++++++++==============",articles)
        # print("==========================++++++++==============",context)
        
        if str(article.category) in ["Qonunlar", "Qarorlar", "Farmonlar", "Standartlar", "Dasturlar", "Loyihalar", "E'lonlar"]:
            return render(request, 'one_page_detail.html', context)
        return render(request, 'article_detail.html', context)
    

class UserDetailView(View):
    def get(self, request,category_id, id):
        # articles = get_object_or_404(Article, category = id)
        article = Article.objects.get(id=int(id))
        article.views += 1  # Ko'rishlar sonini 1 ga oshirish
        article.save()
      
        context = {
            'category_id':category_id,
            'article':article,
            }
        # print("==========================++++++++==============",articles)
        # print("==========================++++++++==============",context)
        
        return render(request, 'one_page_detail.html', context)

