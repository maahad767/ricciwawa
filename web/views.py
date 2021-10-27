import requests
from django.shortcuts import render, redirect
from django.views import generic


# directly inherited from Kenneth Yip
class Home(generic.TemplateView):
    template_name = 'web/homepage.html'


class Resources(generic.TemplateView):
    template_name = 'web/resources.html'

    def get_context_data(self, *args, **kwargs):
        context = {
            'show_home': True,
            'show_resources': False,
            'show_ricciwawa_text': True,
            'bar_image': "ricciwawa_logo.svg",
            'bar_color': "#FFA500",
            'title': "Ricciwawa Ricci娃娃",
        }
        return context


class Blog(generic.TemplateView):
    template_name = 'web/blog.html'


class BlogSingle(generic.View):

    def get(self, request, blog_number, *args, **kwargs):

        return render(request, f'web/blog/{blog_number}.html')


class QuestionAnswer(generic.TemplateView):
    template_name = 'web/qna.html'


class Subscription(generic.TemplateView):
    template_name = 'web/subscription.html'


class Contact(generic.View):
    template_name = 'web/contact_us.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        body = [request.kwargs.get('name'), request.kwargs.get('email'),
                "<br />".join(request.kwargs.get('message').split("\n"))]
        body = "<br>".join(body)

        url = 'https://api.mailjet.com/v3.1/send'
        headers = {'Content-Type': 'application/json', }

        message = {"Messages": [{"From": {"Email": "alaminkouser01@gmail.com", "Name": "Visitor"}, "To": [
            {"Email": "info@ricciwawa.com", "Name": "Info"}], "Subject": "", "TextPart": "", "HTMLPart": ""}]}
        message["Messages"][0]["Subject"] = "Contact Form Data"
        message["Messages"][0]["TextPart"] = body
        message["Messages"][0]["HTMLPart"] = body
        requests.post(url, headers=headers, json=message,
                      auth=('15eed47ea49c8eddd28ca63b1607a072', 'a7b436bd3bd17ebf09730aef770b95c0'))

        return redirect('web:home')


class EditContent(generic.TemplateView):
    template_name = 'web/index_edit.html'

    def get_context_data(self, **kwargs):
        context = {
            'show_ricciwawa_text': True,
            'show_home': True,
            'show_resources': True,
            'bar_image': "wawa_logo.svg",
            'bar_color': "#FFA500",
            'title': "Ricciwawa Ricci娃娃",
            'show_chinese': "inline",
        }
        return context


class TermsOfService(generic.TemplateView):
    template_name = 'web/terms-of-service.html'


class PrivacyPolicy(generic.TemplateView):
    template_name = 'web/privacy-policy.html'



