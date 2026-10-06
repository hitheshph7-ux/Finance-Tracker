from os import error
from django.shortcuts import render
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model, authenticate, login, logout

from .models import Income, Category, Expense

User = get_user_model()


@csrf_exempt
def register(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            email = data.get('email', '')

            if not username or not password:
                return JsonResponse({'error': 'Username and password are required'}, status=400)

            if User.objects.filter(username=username).exists():
                return JsonResponse({'error': 'Username already exist.'}, status=400)

            user = User.objects.create_user(
                username=username,
                password=password,
                email=email
            )

            return JsonResponse({
                'message': 'User registered successfully',
                'user_id': user.id
            }, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data.'}, status=400)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Only POST method is allowed.'}, status=405)


@csrf_exempt
def login_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            username = data.get('username')
            password = data.get('password')

            if not username or not password:
                return JsonResponse({'error': 'Username and password are required.'}, status=400)

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return JsonResponse({'message': 'Login successful!'}, status=200)

            return JsonResponse({'error': 'Invalid credentials.'}, status=401)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data.'}, status=400)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Only POST method is allowed.'}, status=405)


@csrf_exempt
def get_all_users_api(request):
    if request.method == 'GET':
        try:
            users = User.objects.all()

            user_data = []

            for user in users:
                user_data.append({
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'bio': getattr(user, 'bio', '')
                })

            return JsonResponse({'users': user_data}, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Only GET method is allowed.'}, status=405)


@csrf_exempt
def get_user_by_username_api(request, username):
    if request.method == 'GET':
        try:
            user = User.objects.get(username=username)

            user_data = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'bio': getattr(user, 'bio', '')
            }

            return JsonResponse({'user': user_data}, status=200)

        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Only GET method is allowed.'}, status=405)


@csrf_exempt
def add_income_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            user = User.objects.get(id=data.get('user_id'))

            income = Income.objects.create(
                user=user,
                source=data.get('source'),
                amount=data.get('amount')
            )

            return JsonResponse({
                'message': 'Income added successfully',
                'income_id': income.id
            }, status=201)

        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Only POST method is allowed.'}, status=405)
    

@csrf_exempt
def get_all_income_api(request):
    if request.method == 'GET':
        try:
            incomes = Income.objects.all()

            income_data = []

            for income in incomes:
                income_data.append({
                    'id': income.id,
                    'user': income.user.username,
                    'source': income.source,
                    'amount': income.amount,
                    'date': income.date
                })

            return JsonResponse({'income': income_data}, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Only GET method is allowed.'}, status=405)


@csrf_exempt
def add_category_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            category = Category.objects.create(
                name=data.get('name')
            )

            return JsonResponse({
                'message': 'Category added successfully',
                'category_id': category.id
            }, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Only POST method is allowed.'}, status=405)


@csrf_exempt
def get_all_category_api(request):
    if request.method == 'GET':
        try:
            categories = Category.objects.all()

            category_data = []

            for category in categories:
                category_data.append({
                    'id': category.id,
                    'name': category.name
                })

            return JsonResponse({'categories': category_data}, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Only GET method is allowed.'}, status=405)

@csrf_exempt
def get_income_by_id_api(request, income_id):
    if request.method == 'GET':
        try:
            income = Income.objects.get(id=income_id)

            income_data = {
                'id': income.id,
                'user': income.user.username,
                'source': income.source,
                'amount': income.amount,
                'date': income.date
            }

            return JsonResponse({'income': income_data}, status=200)

        except Income.DoesNotExist:
            return JsonResponse({'error': 'Income not found'}, status=404)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Only GET method is allowed.'}, status=405)


@csrf_exempt
def update_income_api(request, income_id):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)

            income = Income.objects.get(id=income_id)

            income.source = data.get('source', income.source)
            income.amount = data.get('amount', income.amount)

            income.save()

            return JsonResponse({
                'message': 'Income updated successfully.'
            }, status=200)

        except Income.DoesNotExist:
            return JsonResponse({'error': 'Income not found'}, status=404)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data.'}, status=400)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Only PUT method is allowed.'}, status=405)


@csrf_exempt
def delete_income_api(request, income_id):
    if request.method == 'DELETE':
        try:
            income = Income.objects.get(id=income_id)

            income.delete()

            return JsonResponse({
                'message': 'Income deleted successfully.'
            }, status=200)

        except Income.DoesNotExist:
            return JsonResponse({'error': 'Income not found'}, status=404)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Only DELETE method is allowed.'}, status=405)


@csrf_exempt
def get_category_by_id_api(request, category_id):
    if request.method == 'GET':
        try:
            category = Category.objects.get(id=category_id)

            category_data = {
                'id': category.id,
                'name': category.name
            }

            return JsonResponse({'category': category_data}, status=200)

        except Category.DoesNotExist:
            return JsonResponse({'error': 'Category not found'}, status=404)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Only GET method is allowed.'}, status=405)


@csrf_exempt
def update_category_api(request, category_id):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)

            category = Category.objects.get(id=category_id)

            category.name = data.get('name', category.name)

            category.save()

            return JsonResponse({
                'message': 'Category updated successfully.'
            }, status=200)

        except Category.DoesNotExist:
            return JsonResponse({'error': 'Category not found'}, status=404)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data.'}, status=400)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Only PUT method is allowed.'}, status=405)


@csrf_exempt
def delete_category_api(request, category_id):
    if request.method == 'DELETE':
        try:
            category = Category.objects.get(id=category_id)

            category.delete()

            return JsonResponse({
                'message': 'Category deleted successfully.'
            }, status=200)

        except Category.DoesNotExist:
            return JsonResponse({'error': 'Category not found'}, status=404)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Only DELETE method is allowed.'}, status=405)