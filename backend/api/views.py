from django.db.models import Sum
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from api.serializers import UserSerializer, BlogSerializer, CommentSerializer
from blog.models import User, Blog, Comment
from blog.pagination import APIViewPageNumberPaginations


def unified_response(code=status.HTTP_200_OK, msg='Success', data=None):
    return {
        'code': code,
        'msg': msg,
        'data': data
    }


class UserViewSet(viewsets.ModelViewSet):
    # pass
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def list(self, request, *args, **kwargs):
        u_id = request.query_params.get('u_id')

        if u_id:
            queryset = User.objects.filter(u_id=u_id)
        else:
            queryset = User.objects.all()
        return JsonResponse(unified_response(data=UserSerializer(queryset, many=True).data))

    def create(self, request, *args, **kwargs):
        try:
            super().create(request)
            return JsonResponse(unified_response(msg=f'用户【{request.data["u_name"]}】注册成功！'))
        except Exception as e:
            return JsonResponse(unified_response(status.HTTP_500_INTERNAL_SERVER_ERROR, msg=f'注册失败！错误信息【{e}】'))

    # @csrf_exempt
    @action(methods=['post'], detail=False)
    def login(self, request, *args, **kwargs):
        user_info = request.data
        try:
            user = User.objects.get(u_name=user_info['name'])
            if user.u_password == user_info['password']:
                return JsonResponse(unified_response(data=UserSerializer(user).data))
            else:
                return JsonResponse(unified_response(status.HTTP_500_INTERNAL_SERVER_ERROR,
                                                     msg=f': 用户名【{user_info["name"]}】密码为空或错误！'))
        except User.DoesNotExist:
            # 用户不存在的处理逻辑
            return JsonResponse(unified_response(status.HTTP_500_INTERNAL_SERVER_ERROR,
                                                 msg=f': 用户名【{user_info["name"]}】为空或错误！'))

    def update(self, request, *args, **kwargs):
        try:
            super().update(request)
            return JsonResponse(unified_response())
        except Exception as e:
            return JsonResponse(unified_response(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e)))


class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer

    def list(self, request, *args, **kwargs):
        u_id = request.query_params.get('u_id')
        title = request.query_params.get('title')

        if u_id and title:
            instance = Blog.objects.filter(u_id=u_id).filter(title__icontains=title)
        elif u_id:
            instance = Blog.objects.filter(u_id=u_id)
        elif title:
            instance = Blog.objects.filter(title__icontains=title)
        else:
            instance = Blog.objects.all()

        # 拿到序列化器
        ser = BlogSerializer

        paginat = APIViewPageNumberPaginations(request, ser, instance)
        # 拿到分页后的数据
        blog_data = paginat.start()

        return JsonResponse(unified_response(data=blog_data))

    def create(self, request, *args, **kwargs):
        super().create(request)
        return JsonResponse(unified_response())

    def destroy(self, request, *args, **kwargs):
        try:
            super().destroy(request)
            return JsonResponse(unified_response())
        except Exception as e:
            return JsonResponse(unified_response(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e)))

    def update(self, request, *args, **kwargs):
        try:
            super().update(request)

            u_id = request.data.get('u_id')
            b_id = int(self.kwargs['pk'])
            likes = request.data.get('likes')

            if u_id and b_id and likes is not None:
                user = User.objects.filter(u_id=u_id).first()
                total_likes = Blog.objects.filter(u_id=u_id).exclude(blog_id=b_id).aggregate(total_likes=Sum('likes'))['total_likes']
                if total_likes:
                    user.total_likes = total_likes + likes
                else:
                    user.total_likes = likes
                user.save()

            return JsonResponse(unified_response())
        except Exception as e:
            return JsonResponse(unified_response(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e)))


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    ordering = ['created_time']  # 默认以创建时间降序排序

    def list(self, request, *args, **kwargs):
        blog_id = request.query_params.get('blog_id')

        if blog_id:
            queryset = Comment.objects.filter(blog_id=blog_id)
        else:
            queryset = Comment.objects.all()
        return JsonResponse(unified_response(data=CommentSerializer(queryset, many=True).data))

    def create(self, request, *args, **kwargs):
        try:
            super().create(request)

            blog_id = request.data.get('blog_id')
            if blog_id:
                blog = Blog.objects.filter(blog_id=blog_id).first()
                blog.comments += 1
                blog.save()

                ser_blog = BlogSerializer
                u_id = ser_blog(blog).data['u_id']

                if u_id:
                    user = User.objects.filter(u_id=u_id).first()
                    user.total_comments += 1
                    user.save()

            return JsonResponse(unified_response())
        except Exception as e:
            return JsonResponse(unified_response(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e)))

    def destroy(self, request, *args, **kwargs):
        try:
            super().destroy(request)
            return JsonResponse(unified_response())
        except Exception as e:
            return JsonResponse(unified_response(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e)))
