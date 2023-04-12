from rest_framework.views import APIView, Response, Request, status
from movies.serializers import MovieSerializer, MovieOrderSerializer
from movies.models import Movie
from rest_framework_simplejwt.authentication import JWTAuthentication
from movies.permissions import IsEmployeeOrReadOnly
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated


class MovieView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsEmployeeOrReadOnly]

    def post(self, request: Request) -> Response:
        serializer = MovieSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save(user=request.user)

        return Response(serializer.data, status.HTTP_201_CREATED)

    def get(self, request: Request) -> Response:
        movies = Movie.objects.all()

        serializer = MovieSerializer(movies, many=True)

        return Response(serializer.data, status.HTTP_200_OK)


class MovieDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsEmployeeOrReadOnly]

    def get(self, request: Request, movie_id: int) -> Response:
        movie = get_object_or_404(Movie, id=movie_id)
        serializer = MovieSerializer(movie)

        return Response(serializer.data, status.HTTP_200_OK)

    def delete(self, request: Request, movie_id: int) -> Response:
        movie = get_object_or_404(Movie, id=movie_id)
        movie.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class MovieOrderView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request: Request, movie_id: int) -> Response:
        serializer = MovieOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        movie = get_object_or_404(Movie, id=movie_id)

        serializer.save(user=request.user, movie=movie)

        return Response(serializer.data, status.HTTP_201_CREATED)
