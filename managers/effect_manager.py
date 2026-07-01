from effects.attack_effect import AttackEffect
from effects.damage_text import DamageText


class EffectManager:
    def __init__(self):
        self.effects = []
        self.damage_texts = []

    def clear(self):
        self.effects = []
        self.damage_texts = []

    def add_attack_effect(self, x, y, damage):
        self.effects.append(AttackEffect(x, y))
        self.damage_texts.append(DamageText(x, y, damage))

    def update(self):
        for effect in self.effects[:]:
            effect.update()

            if effect.is_finished():
                self.effects.remove(effect)

        for damage_text in self.damage_texts[:]:
            damage_text.update()

            if damage_text.is_finished():
                self.damage_texts.remove(damage_text)

    def draw(self, screen):
        for effect in self.effects:
            effect.draw(screen)

        for damage_text in self.damage_texts:
            damage_text.draw(screen)