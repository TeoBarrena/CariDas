import pandas as pd   
import matplotlib.pyplot as plt
import io
import base64
import matplotlib
import numpy as np
from django.shortcuts import render
from Trueques.models import Trueque  # Asegúrate de importar el modelo Trueque adecuadamente
from django.contrib.auth.decorators import login_required, user_passes_test
from functools import wraps
from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.db.models import Count
from accounts.models import Usuario
from.utils import render_to_pdf

# Utilizar un backend adecuado para entornos web
matplotlib.use('Agg')

context = {}

def user_authenticated(user):
    return user.is_authenticated

def user_is_specific_user(user_id):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.id == user_id:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponseForbidden("No tienes permiso para acceder a esta página.")
        return _wrapped_view
    return decorator

@login_required
@user_passes_test(user_authenticated)
@user_is_specific_user(user_id=1)
def obtener_valores(request, area_chart_type='edades'): ## necesario este metodo para el pdf
    # Obtener todos los trueques con estados definidos
    trueques = Trueque.objects.filter(estado_trueque__in=['Pendiente', 'Aceptado', 'Rechazado', 'Eliminado', 'Completado']).values('estado_trueque')

    # Definir los posibles estados de trueque
    ESTADO_TRUEQUE = [('Pendiente', 'Pendiente'), ('Aceptado','Aceptado'),
                      ('Rechazado', 'Rechazado'), ('Eliminado', 'Eliminado'),
                      ('Completado', 'Completado')]

    # Inicializar variables de gráficos
    bar_chart = None
    pie_chart = None
    area_chart = None
    stats_summary = None

    # Verificar que existen datos
    if trueques.exists():
        df = pd.DataFrame(trueques)

        # Verificar y manejar NaNs en el DataFrame
        df['estado_trueque'] = df['estado_trueque'].fillna('desconocido')

        # Contar la cantidad de cada estado
        counts = df['estado_trueque'].value_counts().reindex([estado for estado, _ in ESTADO_TRUEQUE], fill_value=0)
        # Calcular porcentajes
        total = counts.sum()
        percentages = [(counts[estado] / total) * 100 if total > 0 else 0 for estado, _ in ESTADO_TRUEQUE]

        stats_summary = {
            'total': total,
            'accepted_percentage': percentages[1],
            'rejected_percentage': percentages[2],
            'cancelled_percentage': percentages[3]
        }

        # Generar gráfico de barras
        fig, ax = plt.subplots()
        labels = [estado for estado, _ in ESTADO_TRUEQUE]
        values = [counts[estado] for estado, _ in ESTADO_TRUEQUE]
        colors = ['green', 'blue', 'red', 'purple', 'orange']
        ax.bar(labels, values, color=colors)
        ax.set_ylabel('Número de Trueques')
        ax.set_title('Estadísticas de Trueques')

        # Guardar gráfico de barras en memoria y convertir a base64
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        bar_chart = base64.b64encode(buf.getvalue()).decode('utf-8')
        plt.close(fig)

        # Generar gráfico de torta
        if any(values):  # Línea importante para evitar el error de NaN float
            fig, ax = plt.subplots()
            
            ax.pie(values, labels=labels, autopct='%1.1f%%', colors=colors)
            ax.set_title('Distribución de Trueques')

            # Guardar gráfico de torta en memoria y convertir a base64
            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)
            pie_chart = base64.b64encode(buf.getvalue()).decode('utf-8')
            plt.close(fig)

        # Gráfico de Áreas
        if area_chart_type == 'edades':
            users = Usuario.objects.all()
            df = pd.DataFrame(users.values('age'))
            df['count'] = 1
            df = df.groupby('age').count().reset_index()

            fig, ax = plt.subplots()
            ax.fill_between(df['age'], df['count'], color='skyblue', alpha=0.4)
            ax.plot(df['age'], df['count'], color='Slateblue', alpha=0.6, linewidth=2)
            ax.set_title('Distribución de Edades de Usuarios')
            ax.set_xlabel('Edad')
            ax.set_ylabel('Número de Usuarios')

            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)
            area_chart = base64.b64encode(buf.getvalue()).decode('utf-8')
            plt.close(fig)
        elif area_chart_type == 'categorias':
            categorias = Trueque.objects.values('categoria__nombre').annotate(count=Count('categoria__nombre')).order_by('categoria__nombre')
            df = pd.DataFrame(categorias)

            fig, ax = plt.subplots()
            ax.fill_between(df['categoria__nombre'], df['count'], color='skyblue', alpha=0.4)
            ax.plot(df['categoria__nombre'], df['count'], color='Slateblue', alpha=0.6, linewidth=2)
            ax.set_title('Distribución de Categorías de Trueques')
            ax.set_xlabel('Categoría')
            ax.set_ylabel('Número de Trueques')
            plt.xticks(rotation=45)

            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)
            area_chart = base64.b64encode(buf.getvalue()).decode('utf-8')
            plt.close(fig)

        context = {
            'stats_summary': stats_summary,
            'bar_chart': bar_chart,
            'pie_chart': pie_chart,
            'area_chart': area_chart,
            'selected_area_chart_type': area_chart_type  # Pasar la selección al contexto
        }
        return context

@login_required
@user_passes_test(user_authenticated)
@user_is_specific_user(user_id=1)
def view_statistics(request):
    # Obtener todos los trueques con estados definidos
    trueques = Trueque.objects.filter(estado_trueque__in=['Pendiente', 'Aceptado', 'Rechazado', 'Eliminado', 'Completado']).values('estado_trueque')

    # Definir los posibles estados de trueque
    ESTADO_TRUEQUE = [('Pendiente', 'Pendiente'), ('Aceptado','Aceptado'),
                      ('Rechazado', 'Rechazado'), ('Eliminado', 'Eliminado'),
                      ('Completado', 'Completado')]

    # Inicializar variables de gráficos
    bar_chart = None
    pie_chart = None
    area_chart = None
    stats_summary = None

    # Verificar que existen datos
    if trueques.exists():
        df = pd.DataFrame(trueques)

        # Verificar y manejar NaNs en el DataFrame
        df['estado_trueque'] = df['estado_trueque'].fillna('desconocido')

        # Contar la cantidad de cada estado
        counts = df['estado_trueque'].value_counts().reindex([estado for estado, _ in ESTADO_TRUEQUE], fill_value=0)
        # Calcular porcentajes
        total = counts.sum()
        percentages = [(counts[estado] / total) * 100 if total > 0 else 0 for estado, _ in ESTADO_TRUEQUE]

        stats_summary = {
            'total': total,
            'accepted_percentage': percentages[1],
            'rejected_percentage': percentages[2],
            'cancelled_percentage': percentages[3]
        }

        # Generar gráfico de barras
        fig, ax = plt.subplots()
        labels = [estado for estado, _ in ESTADO_TRUEQUE]
        values = [counts[estado] for estado, _ in ESTADO_TRUEQUE]
        colors = ['green', 'blue', 'red', 'purple', 'orange']
        ax.bar(labels, values, color=colors)
        ax.set_ylabel('Número de Trueques')
        ax.set_title('Estadísticas de Trueques')

        # Guardar gráfico de barras en memoria y convertir a base64
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        bar_chart = base64.b64encode(buf.getvalue()).decode('utf-8')
        plt.close(fig)

        # Generar gráfico de torta
        if any(values):  # Línea importante para evitar el error de NaN float
            fig, ax = plt.subplots()
            ax.pie(values, labels=labels, autopct='%1.1f%%', colors=colors)
            ax.set_title('Distribución de Trueques')

            # Guardar gráfico de torta en memoria y convertir a base64
            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)
            pie_chart = base64.b64encode(buf.getvalue()).decode('utf-8')
            plt.close(fig)

        # Gráfico de Áreas
        area_chart_type = request.GET.get('area_chart_type', 'edades')
        if area_chart_type == 'edades':
            users = Usuario.objects.all()
            df = pd.DataFrame(users.values('age'))
            df['count'] = 1
            df = df.groupby('age').count().reset_index()

            fig, ax = plt.subplots()
            ax.fill_between(df['age'], df['count'], color='skyblue', alpha=0.4)
            ax.plot(df['age'], df['count'], color='Slateblue', alpha=0.6, linewidth=2)
            ax.set_title('Distribución de Edades de Usuarios')
            ax.set_xlabel('Edad')
            ax.set_ylabel('Número de Usuarios')

            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)
            area_chart = base64.b64encode(buf.getvalue()).decode('utf-8')
            plt.close(fig)
        elif area_chart_type == 'categorias':
            categorias = Trueque.objects.values('categoria__nombre').annotate(count=Count('categoria__nombre')).order_by('categoria__nombre')
            df = pd.DataFrame(categorias)

            fig, ax = plt.subplots()
            ax.fill_between(df['categoria__nombre'], df['count'], color='skyblue', alpha=0.4)
            ax.plot(df['categoria__nombre'], df['count'], color='Slateblue', alpha=0.6, linewidth=2)
            ax.set_title('Distribución de Categorías de Trueques')
            ax.set_xlabel('Categoría')
            ax.set_ylabel('Número de Trueques')
            plt.xticks(rotation=45)

            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)
            area_chart = base64.b64encode(buf.getvalue()).decode('utf-8')
            plt.close(fig)

        context = {
            'stats_summary': stats_summary,
            'bar_chart': bar_chart,
            'pie_chart': pie_chart,
            'area_chart': area_chart,
            'selected_area_chart_type': area_chart_type  # Pasar la selección al contexto
        }
    else:
        context = {'message': 'No hay datos suficientes para realizar las estadísticas del sistema'}

    return render(request, 'view_statistics.html', context)

def estadisticas_pdf(request):
    area_chart_type = request.GET.get('area_chart_type', 'edades')  # Obtener el tipo de gráfico de áreas del request
    context = obtener_valores(request, area_chart_type)  # Pasar el tipo de gráfico a la función obtener_valores
    return render_to_pdf('estadistica_pdf.html', context)