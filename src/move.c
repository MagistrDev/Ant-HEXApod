/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   move.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: bdrinkin <bdrinkin@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2021/05/26 23:29:38 by bdrinkin          #+#    #+#             */
/*   Updated: 2021/05/27 02:06:36 by bdrinkin         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "antmen.h"

// t_vec	goStraight() {
	
// }

// t_vec	goBack() {
	
// }

// t_vec	goLeft() {
	
// }

// t_vec	goRight() {
	
// }

static bool process_advanced_trajectory(float motion_time) {

	// Check curvature value
	float curvature = (float)g_currentTrajectoryConfig.curvature / 1000.0f;
	
	if (g_currentTrajectoryConfig.curvature == 0)
		curvature = +0.001f;
	if (g_currentTrajectoryConfig.curvature > 1999)
		curvature = +1.999f;
	if (g_currentTrajectoryConfig.curvature < -1999)
		curvature = -1.999f;
	//
	// Calculate XZ
	//
	const float distance = (float)g_currentTrajectoryConfig.distance;

	// Calculation radius of curvature
	const float curvature_radius = tanf((2.0f - curvature) * M_PI / 4.0f) * distance;

	// Common calculations
	float trajectory_radius[SUPPORT_LIMBS_COUNT] = {0};
	float start_angle_rad[SUPPORT_LIMBS_COUNT] = {0};
	float max_trajectory_radius = 0;
	for (uint32_t i = 0; i < SUPPORT_LIMBS_COUNT; ++i) {
		
		const float x0 = g_motionConfig.startPositions[i].x;
		const float z0 = g_motionConfig.startPositions[i].z;

		// Calculation trajectory radius
		trajectory_radius[i] = sqrtf((curvature_radius - x0) * (curvature_radius - x0) + z0 * z0);

		// Search max trajectory radius
		if (trajectory_radius[i] > max_trajectory_radius) {
			max_trajectory_radius = trajectory_radius[i];
		}

		// Calculation limb start angle
		start_angle_rad[i] = atan2f(z0, -(curvature_radius - x0));
	}
	if (max_trajectory_radius == 0) {
		return false; // Avoid division by zero
	}

	// Calculation max angle of arc
	const int32_t curvature_radius_sign = (curvature_radius >= 0) ? 1 : -1;
	const float max_arc_angle = curvature_radius_sign * distance / max_trajectory_radius;

	// Calculation points by time
	for (uint32_t i = 0; i < SUPPORT_LIMBS_COUNT; ++i) {
		
		// Inversion motion time if need
		float relative_motion_time = motion_time;
		if (g_motionConfig.timeDirections[i] == TIME_DIR_REVERSE) {
			relative_motion_time = 1.0f - relative_motion_time;
		}

		// Calculation arc angle for current time
		const float arc_angle_rad = (relative_motion_time - 0.5f) * max_arc_angle + start_angle_rad[i];

		// Calculation XZ points by time
		g_limbsList[i].x = curvature_radius + trajectory_radius[i] * cosf(arc_angle_rad);
		g_limbsList[i].z = trajectory_radius[i] * sinf(arc_angle_rad);
		
		// Calculation Y points by time
		if (g_motionConfig.trajectories[i] == TRAJECTORY_XZ_ADV_Y_CONST) {
			g_limbsList[i].y = g_motionConfig.startPositions[i].y;
		}
		else if (g_motionConfig.trajectories[i] == TRAJECTORY_XZ_ADV_Y_SINUS) {
			g_limbsList[i].y = g_motionConfig.startPositions[i].y;
			g_limbsList[i].y += LIMB_STEP_HEIGHT * sinf(relative_motion_time * M_PI);  
		}
	}
	return true;
}

void	init_hexapod(void) {
	
	g_currentTrajectoryConfig.curvature = 500;
	g_currentTrajectoryConfig.distance = 50;
	// стартовые позиции
	g_motionConfig.startPositions[0] = (t_vec){-80, -50, 0};
	g_motionConfig.startPositions[1] = (t_vec){-70,-50, -70};
	g_motionConfig.startPositions[2] = (t_vec){70, -50, 70};
	g_motionConfig.startPositions[3] = (t_vec){80, -50, 0};
	g_motionConfig.startPositions[4] = (t_vec){80, -50, 0};
	g_motionConfig.startPositions[5] = (t_vec){70, -50, -70};
	
	g_motionConfig.timeDirections[0] = 1;
	g_motionConfig.timeDirections[1] = 0;
	g_motionConfig.timeDirections[2] = 1;
	g_motionConfig.timeDirections[3] = 0;
	g_motionConfig.timeDirections[4] = 1;
	g_motionConfig.timeDirections[5] = 0;
	
	g_motionConfig.trajectories[0] = 0;
	g_motionConfig.trajectories[1] = 1;
	g_motionConfig.trajectories[2] = 0;
	g_motionConfig.trajectories[3] = 1;
	g_motionConfig.trajectories[4] = 0;
	g_motionConfig.trajectories[5] = 1;
	
	for (int i = 0; i < SUPPORT_LIMBS_COUNT; i++) {
		g_limbsList[i] = g_motionConfig.startPositions[i];
	}
}

# include <stdio.h>

static void	printVec(t_vec v) {
	printf("\tVector.x = %f\n\tVector.y = %f\n\tVector.z = %f\n", v.x, v.y, v.y);
}

int		main(void) {
	init_hexapod();
	for (int i = 0; i < 5; i++) {
		printf("___________Step %d____________\n", i);
		if (process_advanced_trajectory(12.f)) {
			for (int i = 0; i < SUPPORT_LIMBS_COUNT; i++) {
				printf("LEG #%d\n", i + 1);
				printVec(g_limbsList[i]);
			}
		} else {
			printf("Some wrong\n");
		}
	}
}