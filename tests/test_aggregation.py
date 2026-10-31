import unittest
from datetime import datetime
from src.ai_coding_trend_analyzer.aggregation import aggregate_commits_by_period

class TestAggregation(unittest.TestCase):
    def setUp(self):
        # 3 weeks, 2 months, mixed agent/human
        self.commit_data = [
            {  # Human
                'timestamp': datetime(2024, 5, 1, 10, 0, 0),
                'agent_keyword_found': False
            },
            {  # Agent
                'timestamp': datetime(2024, 5, 2, 12, 30, 0),
                'agent_keyword_found': True
            },
            {  # Agent
                'timestamp': datetime(2024, 5, 3, 15, 45, 0),
                'agent_keyword_found': True
            },
            {  # Human, different week
                'timestamp': datetime(2024, 5, 10, 9, 0, 0),
                'agent_keyword_found': False
            },
            {  # Human, different month
                'timestamp': datetime(2024, 6, 1, 8, 0, 0),
                'agent_keyword_found': False
            },
            {  # Agent, same month as above
                'timestamp': datetime(2024, 6, 2, 14, 0, 0),
                'agent_keyword_found': True
            },
        ]

    def test_aggregate_by_week(self):
        result = aggregate_commits_by_period(self.commit_data, period='week')
        # Check keys are week strings
        for key in result:
            self.assertRegex(key, r'^2024-W\\d{2}$')
        # Check counts
        total = sum(period['total'] for period in result.values())
        agent = sum(period['agent'] for period in result.values())
        human = sum(period['human'] for period in result.values())
        self.assertEqual(total, 6)
        self.assertEqual(agent, 3)
        self.assertEqual(human, 3)
        # Each period's total = agent + human
        for period in result.values():
            self.assertEqual(period['total'], period['agent'] + period['human'])

    def test_aggregate_by_month(self):
        result = aggregate_commits_by_period(self.commit_data, period='month')
        # Should be two months: 2024-05 and 2024-06
        self.assertIn('2024-05', result)
        self.assertIn('2024-06', result)
        self.assertEqual(result['2024-05']['total'], 4)
        self.assertEqual(result['2024-05']['agent'], 2)
        self.assertEqual(result['2024-05']['human'], 2)
        self.assertEqual(result['2024-06']['total'], 2)
        self.assertEqual(result['2024-06']['agent'], 1)
        self.assertEqual(result['2024-06']['human'], 1)

    def test_handles_malformed_entries(self):
        # Missing timestamp or wrong type
        bad_data = [
            {'timestamp': 'not-a-datetime', 'agent_keyword_found': True},
            {'agent_keyword_found': False},
        ]
        result = aggregate_commits_by_period(bad_data, period='week')
        self.assertEqual(result, {})

    def test_invalid_period_raises(self):
        with self.assertRaises(ValueError):
            aggregate_commits_by_period(self.commit_data, period='year')

if __name__ == '__main__':
    unittest.main()
