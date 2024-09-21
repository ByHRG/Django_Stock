from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt
from myapp.utills.kasina import KASINA

NextID = 2
topics = [{
    'id': 1,
    'title': 'StockList',
    'body': '''재고 조회'''
    }
]
def HTMLTemplate(articleTag):
    global topics
    ol = ''
    for topic in topics:
        ol += f'<li><a href="/read/{topic["id"]}">{topic["title"]}</a></li>'

    return f'''
    <html>
    <body>
        <h1><a href="/">StockChecker</a></h1>
        <ul>
            {ol}
        </ul>
        {articleTag}
        <ul>
            <li><a href="/create/">create</a></li>
        </ul>
    </body>
    </html>
    '''

def index(request):
    article = '''
    <h2>Welcome</h2>
    Hello, Django
    '''
    return HttpResponse(HTMLTemplate(article))

@csrf_exempt
def create(request):
    global NextID
    if request.method == 'GET':
        article = '''
        <form action="/create/" method="post">
            <p><input type="text" name="url" placeholder="https://www.kasina.co.kr/product-detail/123245137"></p>
            <p><input type="submit"></p>
        </form>
        '''
        return HttpResponse(HTMLTemplate(article))
    elif request.method == "POST":
        data = KASINA().run(request.POST['url'])
        body = f'<a href="{data["Url"]}">{data["Url"]}</a>'
        for i in data["Stock"]:
            body += f'<p>{i} - {data["Stock"][i]}</p>'

        newTopic = {"id": NextID,"title": data["Model"]+" "+data["Name"], "body": body}
        url = '/read/'+str(NextID)
        topics.append(newTopic)
        NextID += 1
        return redirect(url)

def read(request, id):
    global topics
    article = ''
    for topic in topics:
        if str(topic['id']) == (id):
            article = f'<h2>{topic["title"]}</h2>{topic["body"]}'
    return HttpResponse(HTMLTemplate(article))
