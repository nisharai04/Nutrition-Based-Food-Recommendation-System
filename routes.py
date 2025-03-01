from flask import Blueprint, render_template, request
from .models import load_data, train_model, get_recommendations, get_image 

data = load_data()
model = train_model(data)

main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
def index():
    """Render the main index page."""
    fibre_g = request.form.get('fibre_g', '')
    cholesterol_mg = request.form.get('cholesterol_mg', '')
    freesugar_g = request.form.get('freesugar_g', '')
    sodium_mg = request.form.get('sodium_mg', '')
    carb_g = request.form.get('carb_g', '')
    energy_kcal = request.form.get('energy_kcal', '')
    fat_g = request.form.get('fat_g', '')
    protein_g = request.form.get('protein_g', '')
    error = request.args.get('error')

    recommendations = None  

    if request.method == 'POST':
        try:
            input_features = [
                float(fibre_g),
                float(cholesterol_mg),
                float(freesugar_g),
                float(sodium_mg),
                float(carb_g),
                float(energy_kcal),
                float(fat_g),
                float(protein_g)
            ]
            recommendations = get_recommendations(model, data, input_features)

            if recommendations is not None:
                recommendations['image_url'] = recommendations['food_name'].apply(get_image)

        except ValueError:
            error = "Invalid input. Please enter numerical values."

    return render_template('index.html',
                           fibre_g=fibre_g,
                           cholesterol_mg=cholesterol_mg,
                           freesugar_g=freesugar_g,
                           sodium_mg=sodium_mg,
                           carb_g=carb_g,
                           energy_kcal=energy_kcal,
                           fat_g=fat_g,
                           protein_g=protein_g,
                           error=error,
                           recommendations=recommendations)

@main.route('/details/<int:food_id>')
def details(food_id):
    """Render details of a specific food item."""
    try:
        item = data.iloc[food_id]
        item['image_url'] = get_image(item['food_name']) 
        return render_template('recipe_details.html', item=item)
    except IndexError:
        return render_template('error.html', message="Food item not found.")