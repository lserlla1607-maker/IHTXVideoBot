import discord
import aiohttp
class DownloadError(Exception):
  pass
async def from_url(url:str, file_name:str):
  async with aiohttp.ClientSession() as session:
    async with session.get(url) as response:
      if response.status == 200:
        with open(file_name, "wb") as f:
          f.write(await response.read())
      else:
        raise DownloadError("Failed to download.")