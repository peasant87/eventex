from django.test import TestCase
from django.shortcuts import resolve_url as r
from eventex.subscriptions.models import Subscription


class SubscriptionDetailGet(TestCase):
    def setUp(self):
        self.obj = Subscription.objects.create(name="Tiago Amaral", cpf="12345678901",
                    email="peasant87@gmail.com", phone="61-98888-5555")
        self.resp = self.client.get(r('subscriptions:detail', self.obj.hashId))

    def test_get(self):
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.resp,
                                'subscriptions/subscription_detail.html')

    def test_context(self):
        subscription = self.resp.context['subscription']
        self.assertIsInstance(subscription, Subscription)

    def test_html(self):
        contents = (self.obj.name,self.obj.cpf, self.obj.phone, self.obj.email)

        with self.subTest():
            for expected in contents:
                self.assertContains(self.resp,expected)


class SubscriptionDetailNotFound(TestCase):
    def test_not_found(self):
        resp = self.client.get(r('subscriptions:detail', '00000000-0000-0000-0000-000000000000'))
        self.assertEqual(404,resp.status_code)