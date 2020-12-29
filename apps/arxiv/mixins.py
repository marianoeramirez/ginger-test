from django.http import Http404, HttpResponseRedirect
from django.views.generic import DetailView


class BaseStartUnstarMixin(DetailView):
    """
    Base class that define the functionality for star or unstar an Article or Author.
    """

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.kwargs["type"] == "unstar":
            self.object.user_starts.remove(self.request.user)
        elif self.kwargs["type"] == "star":
            self.object.user_starts.add(self.request.user)
        else:
            raise Http404()
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))