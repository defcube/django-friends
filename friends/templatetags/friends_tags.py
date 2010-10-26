from django.template import Library, TemplateSyntaxError, Node
import friends.models

register = Library()

@register.tag
def friends_pending_invite_count(parser, token):
    parts = token.contents.split()
    if len(parts) != 3 or parts[1] != "as":
        raise TemplateSyntaxError(
            "Call as 'friends_pending_invite_count as somevar'")
    return FriendsPendingInviteCountNode(parts[2])
        
class FriendsPendingInviteCountNode(Node):
    ACTIVITY = object()
    OBJECT = object()
    def __init__(self, varname):
        self.varname = varname
        
    def render(self, context):    
        user = context['request'].user
        c = friends.models.FriendshipInvitation.objects.\
          invitations(to_user=user).count()
        context[self.varname] = c
        return ''