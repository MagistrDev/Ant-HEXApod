/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   antmen.h                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: bdrinkin <bdrinkin@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2021/05/26 23:18:53 by bdrinkin          #+#    #+#             */
/*   Updated: 2021/05/27 00:45:41 by bdrinkin         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef ANTMEN_H
# define ANTMEN_H
# include <stdlib.h>
# include <stdint.h>
# include <stdbool.h>
# include <math.h>

# define SUPPORT_LIMBS_COUNT  6
# define TIME_DIR_REVERSE  1
# define TRAJECTORY_XZ_ADV_Y_CONST  0
# define TRAJECTORY_XZ_ADV_Y_SINUS  1
// Высота шага константа меняй через нее
# define LIMB_STEP_HEIGHT  10
# define HEXAPOD_DIRECTION = 0

typedef struct s_currentTrajectoryConfig	t_currentTrajectoryConfig;
typedef struct s_vec						t_vec;
typedef struct s_motionConfig				t_motionConfig;

struct s_vec {
	float	x;
	float	y;
	float	z;
};

struct s_currentTrajectoryConfig {
	float	curvature;
	float	distance;
};

struct s_motionConfig {
	t_vec		startPositions[SUPPORT_LIMBS_COUNT];
	uint32_t	timeDirections[SUPPORT_LIMBS_COUNT];
	uint32_t	trajectories[SUPPORT_LIMBS_COUNT];
};

struct s_limbsList {
	t_vec	position;
};

typedef t_vec	t_limbsList[SUPPORT_LIMBS_COUNT];

t_currentTrajectoryConfig	g_currentTrajectoryConfig = (t_currentTrajectoryConfig){0};
t_motionConfig 				g_motionConfig = (t_motionConfig){0};
t_limbsList					g_limbsList = (t_limbsList){0};

#endif
