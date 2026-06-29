from django.urls import path
from .views import ExportarInscritosView, ExportarPagosView, ExportarDocumentacionView, ExportarInformePDFView, ExportarFichaPDFView

urlpatterns = [
    path('<uuid:viaje_id>/exportar/inscritos/', ExportarInscritosView.as_view(), name='exportar-inscritos'),
    path('<uuid:viaje_id>/exportar/pagos/', ExportarPagosView.as_view(), name='exportar-pagos'),
    path('<uuid:viaje_id>/exportar/documentacion/', ExportarDocumentacionView.as_view(), name='exportar-documentacion'),
    path('<uuid:viaje_id>/exportar/informe-pdf/', ExportarInformePDFView.as_view(), name='exportar-informe-pdf'),
    path('inscripciones/<uuid:inscripcion_id>/resumen-pdf/', ExportarFichaPDFView.as_view(), name='exportar-ficha-pdf'),
]