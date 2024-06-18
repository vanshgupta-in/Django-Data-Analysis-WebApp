from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from .forms import UploadFileForm
from .models import UploadedFile
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import os
import io
import base64

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save()
            return redirect('analyze_file', file_id=uploaded_file.id)
    else:
        form = UploadFileForm()
    return render(request, 'analysis/upload.html', {'form': form})


def analyze_file(request, file_id):
    uploaded_file = UploadedFile.objects.get(id=file_id)
    file_path = uploaded_file.file.path

    # Read the CSV file
    data = pd.read_csv(file_path)

    # Perform basic data analysis
    head = data.head()
    description = data.describe()
    missing_values = data.isnull().sum().to_frame('missing_values')

    # Generate visualizations
    sns.set(style="darkgrid")

    # Store the histograms in base64 encoded strings
    histograms = []
    for column in data.select_dtypes(include=[np.number]).columns:
        fig, ax = plt.subplots()
        sns.histplot(data[column].dropna(), kde=True, ax=ax)
        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)
        image_base64 = base64.b64encode(buf.read()).decode('utf-8')
        histograms.append(image_base64)
        plt.close(fig)  # Close the figure to avoid memory issues

    context = {
        'head': head.to_html(),
        'description': description.to_html(),
        'missing_values': missing_values.to_html(),
        'histograms': histograms,
    }

    return render(request, 'analysis/analyze.html', context)