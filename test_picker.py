import flet as ft
import asyncio

async def main(page: ft.Page):
    async def pick(e):
        print("Picking...")
        fp = ft.FilePicker()
        page.overlay.append(fp)
        page.update()
        res = await fp.pick_files()
        print(f"Result: {res}")

    page.add(ft.ElevatedButton("Test", on_click=pick))

if __name__ == "__main__":
    ft.app(target=main)
