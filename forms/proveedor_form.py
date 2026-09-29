from flask_wtf import FlaskForm
from wtforms import StringField, TelField, EmailField, SubmitField
from wtforms.validators import DataRequired, Length, Email


class ProveedorForm(FlaskForm):

    empresa = StringField(
        "Empresa",
        validators=[
            DataRequired(
                message="El nombre de la empresa es obligatorio."
            ),
            Length(
                min=3,
                max=100,
                message="La empresa debe tener entre 3 y 100 caracteres."
            )
        ]
    )

    producto = StringField(
        "Producto suministrado",
        validators=[
            DataRequired(
                message="El producto suministrado es obligatorio."
            ),
            Length(
                min=2,
                max=100,
                message="El producto debe tener entre 2 y 100 caracteres."
            )
        ]
    )

    telefono = TelField(
        "Teléfono",
        validators=[
            DataRequired(
                message="El teléfono es obligatorio."
            ),
            Length(
                min=7,
                max=15,
                message="El teléfono debe tener entre 7 y 15 caracteres."
            )
        ]
    )

    email = EmailField(
        "Correo electrónico",
        validators=[
            DataRequired(
                message="El correo es obligatorio."
            ),
            Email(
                message="Ingrese un correo válido."
            )
        ]
    )

    submit = SubmitField("Guardar proveedor")
