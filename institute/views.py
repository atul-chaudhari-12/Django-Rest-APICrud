from django.views.generic.base import TemplateView
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from college.staff.forms import PrincipleSignUpForm
from django.views.generic import FormView, CreateView, ListView

class GetTemplate(TemplateView):
    
    def get(self,request,*args,**kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)
    
    
class GenericView(TemplateView):

    """
    Purpose: A generic template view that renders a specified template. The
    template to be rendered is calculated from the url kwargs 'template_name'.
    """
                
    def get_template_names(self):
        """
        Purpose: Get the template name to be rendered.
        :return: return the template name depending upon the url kwargs.
        """
#         import ipdb
#         ipdb.set_trace()
        response_template=None
        if  self.kwargs.get('template_name') in ['princysignup',]:
            response_template=self.kwargs.get('template_name')+".html"
        else:
            response_template=self.kwargs.get('template_name')+".html"
        return response_template 
    
    
class GenericFormView(FormView):

    """
    Purpose: A generic template view that renders a specified form. The
    form to be rendered is calculated from the url kwargs 'template_name'.
    """

    def get_template_names(self):
        
        """
        Purpose: Get the template name to be rendered.
        :return: return the template name depending upon the url kwargs.
        """
        if self.form_name == 'princysignup':
            response_template = [self.kwargs.get('template_name')+".html"]
        self.get_context_data({'form_name':self.form_name})
        return response_template
            
    def get_context_data(self, **kwargs):
        
        kwargs = self.kwargs
        context = super(GenericFormView, self).get_context_data(**kwargs)
        if self.kwargs['form_name'] in ['princysignup', 'buyersguide']:
            context['form']=  PrincipleSignUpForm
            
        return context