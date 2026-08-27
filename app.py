from flask import Flask, request, jsonify
from PIL import Image
from google import genai

app = Flask(__name__)

# إعداد العميل باستخدام مفتاحك
client = genai.Client(api_key="AQ.Ab8RN6KOB7-d6Po8TT0fqcfC2cyndhlvZZ2o8830eIh55rdrGA")

@app.route('/analyze', methods=['POST'])
def analyze_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400
    
    file = request.files['image']
    
    try:
        # فتح الصورة والتعامل معها بوضوح
        image = Image.open(file.stream)
        prompt = "وصِف هذه الصورة بالتفصيل باللغة العربية واستخرج أهم العناصر الموجودة فيها"
        
        # استخدام موديل مدعوم ومستقر لتحليل الصور
        response = client.models.generate_content(
            model='gemini-1.5-pro',
            contents=[prompt, image]
        )
        
        return jsonify({'description': response.text})
        
    except Exception as e:
        # طباعة الخطأ بالتفصيل في التيرمنال لمتابعته لو حصل أي استثناء
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
