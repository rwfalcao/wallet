def main_context_processor(request):
    """
    Essa função é chamada no fim do processamento de cada view
    """
    ctx = dict(
        super_template='base.html'
    )

    return ctx