from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    DateField,
    FloatField,
    IntegerField,
    SelectField,
    SubmitField
)

from wtforms.validators import DataRequired, NumberRange


class FacturacionForm(FlaskForm):

    # ==========================================
    # NÚMERO DE FACTURA
    # ==========================================

    numero_factura = StringField(
        "Número de factura",
        validators=[
            DataRequired(
                message="El número de factura es obligatorio."
            )
        ]
    )

    # ==========================================
    # CLIENTE
    # ==========================================

    cliente = SelectField(
        "Cliente",
        coerce=int,
        validators=[
            DataRequired(
                message="Seleccione un cliente."
            )
        ]
    )

    # ==========================================
    # FECHA
    # ==========================================

    fecha = DateField(
        "Fecha",
        validators=[
            DataRequired(
                message="La fecha es obligatoria."
            )
        ],
        format="%Y-%m-%d"
    )

    # ==========================================
    # PRODUCTO
    # ==========================================

    producto = SelectField(
        "Producto",
        coerce=int,
        validators=[
            DataRequired(
                message="Seleccione un producto."
            )
        ]
    )

    # ==========================================
    # CANTIDAD
    # ==========================================

    cantidad = IntegerField(
        "Cantidad",
        validators=[
            DataRequired(
                message="La cantidad es obligatoria."
            ),
            NumberRange(
                min=1,
                message="La cantidad debe ser mayor que 0."
            )
        ]
    )

    # ==========================================
    # PRECIO UNITARIO
    # ==========================================

    precio = FloatField(
        "Precio unitario",
        validators=[
            DataRequired(
                message="El precio es obligatorio."
            ),
            NumberRange(
                min=0.01,
                message="El precio debe ser mayor que 0."
            )
        ]
    )

    # ==========================================
    # ESTADO
    # ==========================================

    estado = SelectField(
        "Estado",
        choices=[
            ("Pagada", "Pagada"),
            ("Pendiente", "Pendiente")
        ],
        validators=[
            DataRequired(
                message="Seleccione un estado."
            )
        ]
    )

    # ==========================================
    # BOTÓN
    # ==========================================

    submit = SubmitField(
        "Guardar factura"
    )