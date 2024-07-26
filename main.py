from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from slides import counter, table, slides, progress_meter

app = FastAPI()

app.include_router(counter.router)
app.include_router(table.router)
app.include_router(slides.router)
app.include_router(progress_meter.router)


@app.get("/", response_class=RedirectResponse)
def read_root():
    return RedirectResponse(url="/slides/0")
