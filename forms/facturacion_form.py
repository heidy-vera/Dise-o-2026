from flask_wtf import FlaskForm
from wtforms import StringField, DateField, FloatField, SelectField, SubmitField
from wtforms.validators import DataRequired, NumberRange


class FacturacionForm(FlaskForm):
    numero_factura = StringField(
        "Número de factura",
        validators=[
            DataRequired(message="El número de factura es obligatorio.")
        ]
    )

    cliente = StringField(
        "Cliente",
        validators=[
            DataRequired(message="El cliente es obligatorio.")
        ]
    )

    fecha = DateField(
        "Fecha",
        validators=[
            DataRequired(message="La fecha es obligatoria.")
        ],
        format="%Y-%m-%d"
    )

    total = FloatField(
        "Total",
        validators=[
            DataRequired(message="El total es obligatorio."),
            NumberRange(min=0.01, message="El total debe ser mayor que 0.")
        ]
    )

    estado = SelectField(
        "Estado",
        choices=[
            ("Pagada", "Pagada"),
            ("Pendiente", "Pendiente")
        ],
        validators=[
            DataRequired(message="Seleccione un estado.")
        ]
    )

    submit = SubmitField("Guardar factura") 