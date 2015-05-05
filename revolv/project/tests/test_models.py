import datetime

from django.test import TestCase
from revolv.base.models import RevolvUserProfile
from revolv.payments.models import (AdminReinvestment, AdminRepayment, Payment,
                                    PaymentType)
from revolv.project.models import Category, Project, ProjectUpdate
from revolv.project.tasks import scrape


class ProjectUpdateTest(TestCase):
    """Tests that check that project updates work with projects"""

    def test_construct(self):
        project = Project.factories.base.create()
        update1 = ProjectUpdate(update_text='This is update text', project=project)
        update2 = ProjectUpdate(update_text='This is another update', project=project)

        # tests basic construction
        self.assertEqual('This is update text', update1.update_text)
        self.assertEqual('This is another update', update2.update_text)

        # tests project relationship
        self.assertEqual(update1.project, update2.project)
        self.assertEqual(update1.project, project)

        update1.save()
        update2.save()
        self.assertEqual(len(ProjectUpdate.objects.all()), 2)

    def test_add_update(self):
        project = Project.factories.base.create()
        project.add_update('Another sample update')
        update = ProjectUpdate.objects.get(update_text='Another sample update')
        self.assertEqual(project, update.project)


class ProjectTests(TestCase):
    """Project model tests."""

    def test_construct(self):
        """Test that we can create a project via factories."""
        test_project = Project.factories.base.build(
            mission_statement="We do solar!",
            impact_power=50.5,
            tagline="Solar is great"
        )
        self.assertEqual(test_project.mission_statement, "We do solar!")
        self.assertEqual(test_project.impact_power, 50.5)
        self.assertEqual(test_project.tagline, "Solar is great")

    def test_save_and_query(self):
        """Test that we can save and then query a project."""
        Project.factories.base.create(
            funding_goal=20.0,
            location="San Francisco",
            mission_statement="Blueprint!",
        )
        entry = Project.objects.all().filter(location="San Francisco")[0]
        self.assertEqual(entry.mission_statement, "Blueprint!")

    def test_aggregate_donations(self):
        """Test that project.amount_donated works."""
        project = Project.factories.base.create(funding_goal=200.0,
                                                amount_donated=0.0,
                                                amount_left=200.0)

        Payment.factories.donation.create(project=project, amount=50.0)
        self.assertEqual(project.amount_donated, 50.0)
        self.assertEqual(project.amount_left, 150.0)

        Payment.factories.donation.create(project=project, amount=25.5)

        done_project = Project.factories.base.create()
        Payment.factories.donation.create(project=done_project,
                                          amount=10.0)
        done_project.complete_project()
        AdminRepayment.factories.base.create(project=done_project, amount=35.0)

        AdminReinvestment.factories.base.create(project=project, amount=25.0)
        AdminReinvestment.factories.base.create(project=project, amount=10.0)
        self.assertEqual(project.amount_donated, 110.5)
        self.assertEqual(project.amount_left, 200.0 - 110.5)
        self.assertEqual(project.rounded_amount_left, int(200.0 - 110.5))

    def test_donors_relation(self):
        """
        Make sure that a user isn't removed from the donors relation of a
        project if he has *multiple* donations to that project but only *one* is
        deleted.
        """
        user = RevolvUserProfile.factories.base.create()
        project = Project.factories.base.create()

        payment1 = Payment.factories.base.create(
            user=user,
            entrant=user,
            payment_type=PaymentType.objects.get_paypal(),
            project=project
        )
        self.assertEquals(project.donors.filter(user=user).count(), 1)

        payment2 = Payment.factories.base.create(
            user=user,
            entrant=user,
            payment_type=PaymentType.objects.get_paypal(),
            project=project
        )
        self.assertEquals(project.donors.filter(user=user).count(), 1)

        payment1.delete()
        self.assertEquals(project.donors.filter(user=user).count(), 1)

        payment2.delete()
        self.assertEquals(project.donors.filter(user=user).count(), 0)

    def test_amount_repaid(self):
        """Test that we calculate the amount repaied on a project correctly."""
        project = Project.factories.base.create(funding_goal=200.0)
        self.assertEqual(project.amount_repaid, 0.0)
        project.complete_project()  # must complete project to make repayments
        AdminRepayment.factories.base.create(project=project, amount=50)
        self.assertEqual(project.amount_repaid, 50.0)
        AdminRepayment.factories.base.create(project=project, amount=60)
        self.assertEqual(project.amount_repaid, 110.0)

    def test_partial_completeness(self):
        """Test that project.partial_completeness works."""
        project = Project.factories.base.create(funding_goal=100.0)
        self.assertEqual(project.partial_completeness, 0.0)
        self.assertEqual(project.partial_completeness_as_js(), "0.0")

        Payment.factories.donation.create(project=project, amount=50.0)
        self.assertEqual(project.partial_completeness, 0.5)

        Payment.factories.donation.create(project=project, amount=25.0)
        self.assertEqual(project.partial_completeness, 0.75)
        self.assertEqual(project.partial_completeness_as_js(), "0.75")

        Payment.factories.donation.create(project=project, amount=25.0)
        self.assertEqual(project.partial_completeness, 1.0)
        self.assertEqual(project.partial_completeness_as_js(), "1.0")

        Payment.factories.donation.create(project=project, amount=25.0)
        self.assertEqual(project.partial_completeness, 1.0)

    def test_days_remaining(self):
        """
        Test that the functions related to the amount of time remaning in
        the project work correctly.
        """
        project = Project.factories.base.build(end_date=datetime.date.today() - datetime.timedelta(days=10))
        self.assertEqual(project.days_left, 10)
        self.assertEqual(project.formatted_days_left(), "10 days left")
        project = Project.factories.base.build(end_date=datetime.date.today() - datetime.timedelta(days=1))
        self.assertEqual(project.days_left, 1)
        self.assertEqual(project.formatted_days_left(), "1 day left")
        project = Project.factories.base.build(end_date=datetime.date.today() - datetime.timedelta(minutes=10, days=0))
        self.assertEqual(project.days_left, 0)
        self.assertEqual(project.formatted_days_left(), Project.LESS_THAN_ONE_DAY_LEFT_STATEMENT)
        project = Project.factories.base.build(end_date=datetime.date.today() + datetime.timedelta(days=1))
        self.assertEqual(project.days_left, 0)
        self.assertEqual(project.formatted_days_left(), Project.NO_DAYS_LEFT_STATEMENT)


class ProjectManagerTests(TestCase):
    """Tests for the Project manager"""

    def setUp(self):
        Project.factories.base.create(org_name="The Community Dance Studio", project_status=Project.ACTIVE)
        Project.factories.base.create(org_name="Comoonity Dairy", project_status=Project.COMPLETED)
        Project.factories.base.create(org_name="Educathing", project_status=Project.PROPOSED)
        Project.factories.base.create(org_name="Fire Emblem", project_status=Project.DRAFTED)

    def test_get_featured(self):
        context = Project.objects.get_featured(1)
        self.assertEqual(len(context), 1)
        self.assertEqual(context[0].org_name, "The Community Dance Studio")

        context = Project.objects.get_featured(10)
        self.assertEqual(len(context), 2)
        self.assertEqual(context[1].org_name, "Comoonity Dairy")

    def test_get_completed(self):
        context = Project.objects.get_completed()
        self.assertEqual(len(context), 1)
        self.assertEqual(context[0].org_name, "Comoonity Dairy")

    def test_get_active(self):
        context = Project.objects.get_active()
        self.assertEqual(len(context), 1)
        self.assertEqual(context[0].org_name, "The Community Dance Studio")

    def test_get_proposed(self):
        context = Project.objects.get_proposed()
        self.assertEqual(len(context), 1)
        self.assertEqual(context[0].org_name, "Educathing")

    def test_get_drafted(self):
        context = Project.objects.get_drafted()
        self.assertEqual(len(context), 1)
        self.assertEqual(context[0].org_name, "Fire Emblem")


class CategoryTest(TestCase):
    """Tests that category selection and updating work with projects."""

    def make_test_categories_and_titles(self, num):
        """
        Create a batch of num Categories from CategoryFactory. Return a tuple
        of those categories and the list of their titles as the last element.
        """
        test_categories = Category.factories.base.create_batch(num)
        return tuple(test_categories) + tuple([[c.title for c in test_categories]])

    def test_update_category(self):
        """ Test that updating a single projects category works """
        project = Project.factories.base.create()
        category1, category2, category_titles = self.make_test_categories_and_titles(2)
        # tests that associating two categories with the project works
        project.update_categories(category_titles[:2])
        self.assertEqual(len(project.category_set.all()), 2)
        self.assertItemsEqual(project.category_set.all(), [category1, category2])
        # tests that having no categories with the project works
        project.update_categories([])
        self.assertEqual(len(project.category_set.all()), 0)

    def test_update_category_multiple_projects(self):
        """ Test that removing categories from a project does not affect other projects """
        # creates 2 projects
        project1, project2 = Project.factories.base.create_batch(2)
        # resets the category factory and makes three categories
        category1, category2, category3, category_titles = self.make_test_categories_and_titles(3)
        # adds categories 1 and 2 to project 1
        project1.update_categories(category_titles[:2])
        self.assertEqual(len(project1.category_set.all()), 2)
        self.assertItemsEqual(project1.category_set.all(), [category1, category2])
        # adds categories 2 and 3 to project 1
        project2.update_categories(category_titles[1:3])
        self.assertEqual(len(project2.category_set.all()), 2)
        self.assertItemsEqual(project2.category_set.all(), [category2, category3])
        # removes category 2 from project 1
        project1.update_categories(category_titles[1:2])
        self.assertEqual(len(project1.category_set.all()), 1)
        self.assertItemsEqual(project1.category_set.all(), [category2])
        # tests that deleting category 2 from project 1 does not affect project 2
        self.assertItemsEqual(project2.category_set.all(), [category2, category3])

    def test_categories_are_always_populated(self):
        """Test that Category.valid_categories always exist in the database initially."""
        for title in Category.valid_categories:
            Category.objects.get(title=title)


class ScrapeTest(TestCase):
    """Test that the scrape task runs with no errors,
        and changes the project's solar data files"""

    def test_scrape(self):
        result = scrape.delay()
        self.assertTrue(result.successful())
