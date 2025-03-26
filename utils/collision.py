def checkPlayerAsteroidCollision(player, asteroids):
    """Check the ship-asteroid collision."""
    for asteroid in asteroids:
        if (player.x < asteroid.x + asteroid.width and 
            player.x + player.width > asteroid.x and 
            player.y < asteroid.y + asteroid.height and 
            player.y + player.height > asteroid.y):
            return True
    return False


def checkBulletAsteroidCollision(player, asteroids, score):
    """Check the bullet-asteroid collision."""
    for asteroid in asteroids[:]:
        for bullet in player.bullets[:]:
            if bullet[0] in range(asteroid.x, asteroid.x + 40) and bullet[1] in range(asteroid.y, asteroid.y + 40):
                asteroids.remove(asteroid)  
                player.bullets.remove(bullet)  
                score += 1  
    return score