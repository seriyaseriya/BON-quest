from effects.attack_effect import AttackEffect
from effects.damage_text import DamageText
from effects.heal_text import HealText


class EffectManager:
    def __init__(self):
        self.effects = []
        self.damage_texts = []
        self.heal_texts = []

    def clear(self):
        self.effects = []
        self.damage_texts = []
        self.heal_texts = []

    def add_attack_effect(self, x, y, damage):
        self.effects.append(AttackEffect(x, y))
        self.damage_texts.append(DamageText(x, y, damage))

    def add_heal_effect(self, x, y, amount):
        self.heal_texts.append(
            HealText(x, y, amount)
        )

    def add_status_text(self, x, y, text, color=(255, 255, 255)):
        from effects.status_text import StatusText

        self.heal_texts.append(
            StatusText(x, y, text, color)
        )

    def update(self):
        for effect in self.effects[:]:
            effect.update()

            if effect.is_finished():
                self.effects.remove(effect)

        for damage_text in self.damage_texts[:]:
            damage_text.update()

            if damage_text.is_finished():
                self.damage_texts.remove(damage_text)

        for heal_text in self.heal_texts[:]:
            heal_text.update()

            if heal_text.is_finished():
                self.heal_texts.remove(heal_text)

    def draw(self, screen):
        for effect in self.effects:
            effect.draw(screen)

        for damage_text in self.damage_texts:
            damage_text.draw(screen)

        for heal_text in self.heal_texts:
            heal_text.draw(screen)