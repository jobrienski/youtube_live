import unittest
from liveapi.services.youtube import YoutubeLiveStreamService

GOOGLE_API_KEY="*************"

class TestYoutubeSearch(unittest.TestCase):
    def test_search_live(self):
        results = YoutubeLiveStreamService.get_livestreams(GOOGLE_API_KEY, max_results=10)
        self.assertIsNotNone(results)
        self.assertTrue(type(results) == list)
        self.assertEqual(len(results), 10)
        for video in results:
            self.assertEqual(set(video.keys()),
                                 {"video_id","title","thumbnail","channel_id","description"})
            self.assertTrue(isinstance(video['thumbnail'], dict))

