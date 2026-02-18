import flet as ft
import firebase_admin
from firebase_admin import credentials, firestore

# Conexão com o Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate("firebase_key.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

def main(page: ft.Page):
    page.title = "Agenda Fabricio & Alessandra"
    page.theme_mode = ft.ThemeMode.DARK
    page.window_width = 450
    page.window_height = 800

    lista_view = ft.ListView(expand=True, spacing=10, padding=20)

    # Função de Sincronização em Tempo Real
    def on_snapshot(col_snapshot, changes, read_time):
        def update_ui():
            lista_view.controls.clear()
            for doc in col_snapshot:
                item = doc.to_dict()
                lista_view.controls.append(
                    ft.ListTile(
                        leading=ft.Icon(ft.icons.CALENDAR_MONTH),
                        title=ft.Text(item.get('titulo', 'Sem título')),
                        subtitle=ft.Text(item.get('data', 'Sem data')),
                    )
                )
            page.update()
        page.run_threadsafe(update_ui)

    # Escuta o Firebase
    db.collection("compromissos").on_snapshot(on_snapshot)

    def salvar_compromisso(e):
        if txt_titulo.value:
            db.collection("compromissos").add({
                "titulo": txt_titulo.value,
                "data": txt_data.value,
                "criado_por": "Fabricio"
            })
            txt_titulo.value = ""
            txt_data.value = ""
            page.update()

    # UI
    txt_titulo = ft.TextField(label="Compromisso", hint_text="O que temos?")
    txt_data = ft.TextField(label="Data/Hora", hint_text="Quando?")
    btn_salvar = ft.ElevatedButton(
        "Adicionar à Agenda", 
        on_click=salvar_compromisso, 
        icon=ft.icons.ADD_CIRCLE # Corrigido aqui
    )

    page.add(
        ft.Text("Nossos Compromissos", size=25, weight="bold"),
        txt_titulo,
        txt_data,
        btn_salvar,
        ft.Divider(),
        lista_view
    )

ft.app(target=main)