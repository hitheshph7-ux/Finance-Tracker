import json
from django.shortcuts import render
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
            username = data.get('username') or data.get('name') or data.get('email')
            password = data.get('password')
            email = data.get('email', '')

            if not username or not password:
                return JsonResponse({'error': 'Username/Name and password are required'}, status=400)

            if User.objects.filter(username=username).exists():
                return JsonResponse({'error': 'Username already exists.'}, status=400)

            user = User.objects.create_user(
                username=username,
                password=password,
                email=email
            )

            return JsonResponse({
                'message': 'User registered successfully',
                'user_id': user.id,
                'username': user.username
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

            username_input = data.get('username') or data.get('email')
            password = data.get('password')

            if not username_input or not password:
                return JsonResponse({'error': 'Username/Email and password are required.'}, status=400)

            user = authenticate(request, username=username_input, password=password)
            if user is None:
                # Try finding user by email
                user_by_email = User.objects.filter(email=username_input).first()
                if user_by_email:
                    user = authenticate(request, username=user_by_email.username, password=password)

            if user is not None:
                login(request, user)
                return JsonResponse({
                    'message': 'Login successful!',
                    'user_id': user.id,
                    'username': user.username
                }, status=200)

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
            user_data = [{'id': u.id, 'username': u.username, 'email': u.email} for u in users]
            return JsonResponse({'users': user_data}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Only GET method is allowed.'}, status=405)


@csrf_exempt
def get_user_by_username_api(request, username):
    if request.method == 'GET':
        try:
            user = User.objects.get(username=username)
            return JsonResponse({'user': {'id': user.id, 'username': user.username, 'email': user.email}}, status=200)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Only GET method is allowed.'}, status=405)


# --- INCOME APIs ---

@csrf_exempt
def add_income_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_id = data.get('user_id')
            source = data.get('source')
            amount = data.get('amount')
            date_val = data.get('date')

            if not source or amount is None:
                return JsonResponse({'error': 'source and amount are required.'}, status=400)

            user = None
            if user_id:
                user = User.objects.filter(id=user_id).first()
            if not user and data.get('username'):
                user = User.objects.filter(username=data.get('username')).first()
            if not user and request.user.is_authenticated:
                user = request.user

            if not user:
                return JsonResponse({'error': 'User not found.'}, status=404)

            kwargs = {'user': user, 'source': source, 'amount': amount}
            if date_val:
                kwargs['date'] = date_val

            income = Income.objects.create(**kwargs)
            return JsonResponse({
                'message': 'Income added successfully',
                'income_id': income.id
            }, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Only POST method is allowed.'}, status=405)


@csrf_exempt
def get_all_income_api(request):
    if request.method == 'GET':
        try:
            user_id = request.GET.get('user_id')
            username = request.GET.get('username')
            incomes = Income.objects.all()
            if user_id:
                incomes = incomes.filter(user_id=user_id)
            elif username:
                incomes = incomes.filter(user__username=username)

            income_data = []
            for inc in incomes:
                income_data.append({
                    'id': inc.id,
                    'user': inc.user.username,
                    'user_id': inc.user.id,
                    'source': inc.source,
                    'amount': float(inc.amount),
                    'date': str(inc.date)
                })

            return JsonResponse({'income': income_data}, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Only GET method is allowed.'}, status=405)


@csrf_exempt
def get_income_by_id_api(request, income_id):
    if request.method == 'GET':
        try:
            inc = Income.objects.get(id=income_id)
            return JsonResponse({
                'income': {
                    'id': inc.id,
                    'user': inc.user.username,
                    'user_id': inc.user.id,
                    'source': inc.source,
                    'amount': float(inc.amount),
                    'date': str(inc.date)
                }
            }, status=200)
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
            inc = Income.objects.get(id=income_id)

            inc.source = data.get('source', inc.source)
            inc.amount = data.get('amount', inc.amount)
            if 'date' in data and data['date']:
                inc.date = data['date']

            inc.save()
            return JsonResponse({'message': 'Income updated successfully.'}, status=200)

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
            inc = Income.objects.get(id=income_id)
            inc.delete()
            return JsonResponse({'message': 'Income deleted successfully.'}, status=200)
        except Income.DoesNotExist:
            return JsonResponse({'error': 'Income not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Only DELETE method is allowed.'}, status=405)


# --- CATEGORY APIs ---

DEFAULT_CATEGORIES = ["Food & Dining", "Rent & Housing", "Shopping", "Transportation", "Entertainment", "Bills & Utilities", "Salary", "Other"]

@csrf_exempt
def add_category_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name')

            if not name:
                return JsonResponse({'error': 'Category name is required.'}, status=400)

            category, created = Category.objects.get_or_create(name=name.strip())
            return JsonResponse({
                'message': 'Category created successfully' if created else 'Category already exists',
                'category_id': category.id,
                'name': category.name
            }, status=201 if created else 200)

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

            # Seed defaults if empty
            if not categories.exists():
                for cat_name in DEFAULT_CATEGORIES:
                    Category.objects.get_or_create(name=cat_name)
                categories = Category.objects.all()

            category_data = [{'id': cat.id, 'name': cat.name} for cat in categories]
            return JsonResponse({'categories': category_data}, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Only GET method is allowed.'}, status=405)


@csrf_exempt
def get_category_by_id_api(request, category_id):
    if request.method == 'GET':
        try:
            cat = Category.objects.get(id=category_id)
            return JsonResponse({'category': {'id': cat.id, 'name': cat.name}}, status=200)
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
            cat = Category.objects.get(id=category_id)

            cat.name = data.get('name', cat.name)
            cat.save()

            return JsonResponse({'message': 'Category updated successfully.'}, status=200)

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
            cat = Category.objects.get(id=category_id)
            cat.delete()
            return JsonResponse({'message': 'Category deleted successfully.'}, status=200)
        except Category.DoesNotExist:
            return JsonResponse({'error': 'Category not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Only DELETE method is allowed.'}, status=405)


# --- EXPENSE APIs ---

@csrf_exempt
def add_expense_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_id = data.get('user_id')
            amount = data.get('amount')
            description = data.get('description', '')
            date_val = data.get('date')

            if amount is None:
                return JsonResponse({'error': 'amount is required.'}, status=400)

            user = None
            if user_id:
                user = User.objects.filter(id=user_id).first()
            if not user and data.get('username'):
                user = User.objects.filter(username=data.get('username')).first()
            if not user and request.user.is_authenticated:
                user = request.user

            if not user:
                return JsonResponse({'error': 'User not found.'}, status=404)

            category_id = data.get('category_id')
            category_name = data.get('category_name')

            if category_id:
                category = Category.objects.get(id=category_id)
            elif category_name:
                category, _ = Category.objects.get_or_create(name=category_name.strip())
            else:
                category, _ = Category.objects.get_or_create(name="General")

            kwargs = {
                'user': user,
                'category': category,
                'amount': amount,
                'description': description
            }
            if date_val:
                kwargs['date'] = date_val

            expense = Expense.objects.create(**kwargs)
            return JsonResponse({
                'message': 'Expense added successfully',
                'expense_id': expense.id
            }, status=201)

        except Category.DoesNotExist:
            return JsonResponse({'error': 'Category not found'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Only POST method is allowed.'}, status=405)


@csrf_exempt
def get_all_expense_api(request):
    if request.method == 'GET':
        try:
            user_id = request.GET.get('user_id')
            username = request.GET.get('username')
            expenses = Expense.objects.all()
            if user_id:
                expenses = expenses.filter(user_id=user_id)
            elif username:
                expenses = expenses.filter(user__username=username)

            expense_data = []
            for exp in expenses:
                expense_data.append({
                    'id': exp.id,
                    'user': exp.user.username,
                    'user_id': exp.user.id,
                    'category': exp.category.name,
                    'category_id': exp.category.id,
                    'amount': float(exp.amount),
                    'description': exp.description,
                    'date': str(exp.date)
                })

            return JsonResponse({'expenses': expense_data}, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Only GET method is allowed.'}, status=405)


@csrf_exempt
def get_expense_by_id_api(request, expense_id):
    if request.method == 'GET':
        try:
            exp = Expense.objects.get(id=expense_id)
            return JsonResponse({
                'expense': {
                    'id': exp.id,
                    'user': exp.user.username,
                    'user_id': exp.user.id,
                    'category': exp.category.name,
                    'category_id': exp.category.id,
                    'amount': float(exp.amount),
                    'description': exp.description,
                    'date': str(exp.date)
                }
            }, status=200)
        except Expense.DoesNotExist:
            return JsonResponse({'error': 'Expense not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Only GET method is allowed.'}, status=405)


@csrf_exempt
def update_expense_api(request, expense_id):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            exp = Expense.objects.get(id=expense_id)

            if 'category_id' in data:
                cat = Category.objects.get(id=data['category_id'])
                exp.category = cat
            elif 'category_name' in data:
                cat, _ = Category.objects.get_or_create(name=data['category_name'].strip())
                exp.category = cat

            exp.amount = data.get('amount', exp.amount)
            exp.description = data.get('description', exp.description)
            if 'date' in data and data['date']:
                exp.date = data['date']

            exp.save()
            return JsonResponse({'message': 'Expense updated successfully.'}, status=200)

        except Expense.DoesNotExist:
            return JsonResponse({'error': 'Expense not found'}, status=404)
        except Category.DoesNotExist:
            return JsonResponse({'error': 'Category not found'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data.'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Only PUT method is allowed.'}, status=405)


@csrf_exempt
def delete_expense_api(request, expense_id):
    if request.method == 'DELETE':
        try:
            exp = Expense.objects.get(id=expense_id)
            exp.delete()
            return JsonResponse({'message': 'Expense deleted successfully.'}, status=200)
        except Expense.DoesNotExist:
            return JsonResponse({'error': 'Expense not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Only DELETE method is allowed.'}, status=405)


# --- TRANSACTION HISTORY API ---

@csrf_exempt
def get_transactions_api(request):
    if request.method == 'GET':
        try:
            user_id = request.GET.get('user_id')
            username = request.GET.get('username')

            incomes_qs = Income.objects.all()
            expenses_qs = Expense.objects.all()

            if user_id:
                incomes_qs = incomes_qs.filter(user_id=user_id)
                expenses_qs = expenses_qs.filter(user_id=user_id)
            elif username:
                incomes_qs = incomes_qs.filter(user__username=username)
                expenses_qs = expenses_qs.filter(user__username=username)

            transactions = []

            for inc in incomes_qs:
                transactions.append({
                    'id': inc.id,
                    'type': 'income',
                    'title': inc.source,
                    'category': 'Income',
                    'amount': float(inc.amount),
                    'date': str(inc.date),
                    'user': inc.user.username,
                    'user_id': inc.user.id
                })

            for exp in expenses_qs:
                transactions.append({
                    'id': exp.id,
                    'type': 'expense',
                    'title': exp.description if exp.description else exp.category.name,
                    'category': exp.category.name,
                    'category_id': exp.category.id,
                    'amount': float(exp.amount),
                    'date': str(exp.date),
                    'user': exp.user.username,
                    'user_id': exp.user.id
                })

            # Sort descending by date and id
            transactions.sort(key=lambda x: (x['date'], x['id']), reverse=True)

            return JsonResponse({'transactions': transactions}, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Only GET method is allowed.'}, status=405)
