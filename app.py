    import os
    import io
    import base64
    import logging
    from datetime import datetime
    from flask import Flask, render_template, request, send_file, flash, redirect, url_for, session
    import qrcode
    from qrcode import QRCode
    from PIL import Image

    # Configure logging
    logging.basicConfig(level=logging.DEBUG)

    # Flask app
    app = Flask(__name__)
    app.secret_key = os.environ.get("SESSION_SECRET", "default_secret_key_for_vercel")

    @app.route('/')
    def index():
        """Render the main QR code generator page"""
        return render_template('index.html')

    @app.route('/generate_qr', methods=['POST'])
    def generate_qr():
        """Generate QR code based on form data and return for preview"""
        try:
            data = request.form.get('data', '').strip()
            fill_color = request.form.get('fill_color', '#000000')
            back_color = request.form.get('back_color', '#ffffff')
            transparent_bg = 'transparent_bg' in request.form
            box_size = int(request.form.get('box_size', 10))
            border = int(request.form.get('border', 4))

            if not data:
                flash('Please enter some data to generate QR code', 'error')
                return redirect(url_for('index'))

            qr = QRCode(
                version=1,
                error_correction=qrcode.ERROR_CORRECT_M,
                box_size=box_size,
                border=border,
            )

            if len(data) > 200:
                flash(f'Long data ({len(data)} characters) will create a dense QR code.', 'warning')

            qr.add_data(data)
            qr.make(fit=True)

            if transparent_bg:
                img = qr.make_image(fill_color=fill_color, back_color=None)
                if img.mode != 'RGBA':
                    img = img.convert('RGBA')
                    data_img = img.getdata()
                    new_data = []
                    for item in data_img:
                        if item[:3] == (255, 255, 255):
                            new_data.append((255, 255, 255, 0))
                        else:
                            new_data.append(item)
                    img.putdata(new_data)
            else:
                img = qr.make_image(fill_color=fill_color, back_color=back_color)

            img_buffer = io.BytesIO()
            img.save(img_buffer, format='PNG')
            img_buffer.seek(0)
            img_base64 = base64.b64encode(img_buffer.getvalue()).decode('utf-8')

            session['qr_data'] = {
                'data': data,
                'fill_color': fill_color,
                'back_color': back_color,
                'transparent_bg': transparent_bg,
                'box_size': box_size,
                'border': border
            }

            return render_template('index.html',
                                   preview_image=img_base64,
                                   form_data=session['qr_data'])

        except Exception as e:
            app.logger.error(f'Error generating QR code: {str(e)}')
            flash('An error occurred while generating the QR code.', 'error')
            return redirect(url_for('index'))


    @app.route('/download_qr')
    def download_qr():
        """Download the generated QR code as PNG file"""
        try:
            if 'qr_data' not in session:
                flash('No QR code to download. Please generate one first.', 'error')
                return redirect(url_for('index'))

            qr_data = session['qr_data']

            qr = QRCode(
                version=1,
                error_correction=qrcode.ERROR_CORRECT_M,
                box_size=qr_data['box_size'],
                border=qr_data['border'],
            )

            qr.add_data(qr_data['data'])
            qr.make(fit=True)

            if qr_data.get('transparent_bg', False):
                img = qr.make_image(fill_color=qr_data['fill_color'], back_color=None)
                if img.mode != 'RGBA':
                    img = img.convert('RGBA')
                    data_img = img.getdata()
                    new_data = []
                    for item in data_img:
                        if item[:3] == (255, 255, 255):
                            new_data.append((255, 255, 255, 0))
                        else:
                            new_data.append(item)
                    img.putdata(new_data)
            else:
                img = qr.make_image(
                    fill_color=qr_data['fill_color'],
                    back_color=qr_data['back_color']
                )

            img_buffer = io.BytesIO()
            img.save(img_buffer, format='PNG')
            img_buffer.seek(0)

            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'qrcode_{timestamp}.png'

            return send_file(
                img_buffer,
                mimetype='image/png',
                as_attachment=True,
                download_name=filename
            )

        except Exception as e:
            app.logger.error(f'Error downloading QR code: {str(e)}')
            flash('An error occurred while downloading the QR code.', 'error')
            return redirect(url_for('index'))


    @app.route('/clear')
    def clear():
        """Clear the current QR code and form data"""
        session.pop('qr_data', None)
        return redirect(url_for('index'))
