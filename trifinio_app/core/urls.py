from django.urls import path

from . import views


urlpatterns = [
    path("", views.dashboard_view, name="dashboard"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("autobuses/", views.autobuses_list, name="autobuses_list"),
    path("autobuses/nuevo/", views.autobuses_crear, name="autobuses_crear"),
    path("autobuses/<int:id_autobus>/editar/", views.autobuses_editar, name="autobuses_editar"),
    path("autobuses/<int:id_autobus>/eliminar/", views.autobuses_eliminar, name="autobuses_eliminar"),
    path("rutas/", views.rutas_list, name="rutas_list"),
    path("rutas/nueva/", views.rutas_crear, name="rutas_crear"),
    path("rutas/<int:id_ruta>/editar/", views.rutas_editar, name="rutas_editar"),
    path("rutas/<int:id_ruta>/eliminar/", views.rutas_eliminar, name="rutas_eliminar"),
    path("pilotos/", views.pilotos_list, name="pilotos_list"),
    path("pilotos/nuevo/", views.pilotos_crear, name="pilotos_crear"),
    path("pilotos/<int:id_piloto>/editar/", views.pilotos_editar, name="pilotos_editar"),
    path("pilotos/<int:id_piloto>/eliminar/", views.pilotos_eliminar, name="pilotos_eliminar"),
    path("viajes/", views.viajes_list, name="viajes_list"),
    path("viajes/nuevo/", views.viajes_crear, name="viajes_crear"),
    path("viajes/<int:id_viaje>/editar/", views.viajes_editar, name="viajes_editar"),
    path("viajes/<int:id_viaje>/eliminar/", views.viajes_eliminar, name="viajes_eliminar"),
    path("viajes/<int:id_viaje>/finalizar/", views.viajes_finalizar, name="viajes_finalizar"),
    path("boletos/vender/", views.boletos_vender, name="boletos_vender"),
    path("encomiendas/registrar/", views.encomiendas_registrar, name="encomiendas_registrar"),
    path("reportes/viajes/", views.reporte_viajes, name="reporte_viajes"),
    path("reportes/ocupacion-rutas/", views.reporte_ocupacion_rutas, name="reporte_ocupacion_rutas"),
    path("reportes/encomiendas/", views.reporte_encomiendas, name="reporte_encomiendas"),
]
