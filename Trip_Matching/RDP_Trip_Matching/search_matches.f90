
!* This code find matching angles and matching routes



subroutine match_angles(path1_angles, path2_angles, angle_tolerance, distance_tolerance, N1, N2, output_array, num_matched)

!f2py   intent(in) :: path1_angles
!f2py   intent(in) :: path2_angles
!f2py   intent(in) :: angle_tolerance
!f2py   intent(in) :: distance_tolerance
!f2py   intent(out) :: output_array
!f2py   intent(out) :: num_matched
!f2py   intent(hide) :: N1
!f2py   intent(hide) :: N2

   real  path1_angles(N1,3)
   real  path2_angles(N2,3)
   real  angle_tolerance
   real  distance_tolerance
   real  output_array(10000,5)

   real angle1
   real angle_diff, dist1_diff, dist2_diff
   integer ifound 
   integer num_matched

   num_matched = 0
   
   Do i = 1, N1   ! loop through all the initial angles
      angle1 = path1_angles(i,1)
      ifound = 0
   
      Do j=1,N2
         angle_diff = abs(path2_angles(j,1) - angle1)
         dist1_diff = abs(path2_angles(j,2) - path1_angles(i,2) )
         dist2_diff = abs(path2_angles(j,3) - path1_angles(i,3) )
   
         if ( ifound .eq. 0  .and. angle_diff .le. angle_tolerance .and. dist1_diff .le. distance_tolerance  &
             .and. dist2_diff .le. distance_tolerance) then
            ifound = j
         end if
   
      End Do
   
      if (ifound .gt. 0) then
         num_matched = num_matched + 1
         output_array( num_matched, 1) = 1   !* this was found
         output_array( num_matched, 2) = i-1   !* this is the angle number of the first path
         output_array( num_matched, 3) = ifound-1   !* this is the angle number of the second path
         output_array( num_matched, 4) = 1.0   !* this is a dummy
         output_array( num_matched, 5) = angle1   !* this is the angle being matched
      end if
   
   
   End Do


return
end




!    # path1 is being compared against path 2
!    for cnt in xrange (0, len(path1.angles)):
!       angle1      = path1.angles[cnt,0]
!       matches = np.where( (abs(path2_angles[:,0]-angle1) <= angle_tolerance)  &  (  abs(path2_angles[:,1]-path1_angles[cnt,1]) <=  16) &  ( abs(path2_angles[:,2]-path1_angles[cnt,2]) <=  16) )
!       if (len(matches[0]) > 0):
!           match_score = [1, cnt, matches[0][0], 1.0, angle1]     # remember this angle
!           match_comparison.append(match_score)       
           
           
           
           
           
           
!      # get the distance between all of the angles
!      self.angle_distances = np.zeros( (len(self.angles), len(self.angles)), dtype=np.float64 )  # start off at zero distance
!
!      for i in range (0, len(self.angles)-1):
!          for j in range(i+1, len(self.angles)):
!         
!              cnt1 = self.angles[i,4]  # the the coordinates of the sorted angles
!              cnt2 = self.angles[j,4]
!          
!              x1, y1 = self.feature_loc[cnt1,0], self.feature_loc[cnt1,1]  # the the coordinates of the sorted angles
!              x2, y2 = self.feature_loc[cnt2,0], self.feature_loc[cnt2,1]
!              distance1 = get_distance(x1,y1,x2,y2)
!
!              self.angle_distances[i,j] = distance1  # remember the distances between these angles
!              self.angle_distances[j,i] = distance1  # remember the distances between these angles           



subroutine calculate_angle_distances(angles, feature_loc,  N1, N2, angle_distances)

!f2py   intent(in) :: angles
!f2py   intent(in) :: feature_loc
!f2py   intent(out) :: angle_distances
!f2py   intent(hide) :: N1
!f2py   intent(hide) :: N2

   real*8  angles(N1,7)
   real*8  feature_loc(N2,3)
   real*8  angle_distances(N1, N1)
   
   integer i,j, cnt1, cnt2
   real*8       x1, y1, x2, y2
   real*8       distance1


   angle_distances = 0

   do i=1,N1-1
      do j= i+1, N1
      
         cnt1 = int(angles(i,5))+1
         cnt2 = int(angles(j,5))+1
         
         !write(6,*) cnt1, cnt2
         !return
         
         x1 = feature_loc(cnt1,1)
         y1 = feature_loc(cnt1,2)

         x2 = feature_loc(cnt2,1)
         y2 = feature_loc(cnt2,2)      
         
         distance1 = ( (x1 - x2)**2 + (y1-y2)**2 )   ** (.5)
         
         angle_distances(i,j) = distance1
         angle_distances(j,i) = distance1
      
      
      end do
   end do



return
end






!               #close_list3.sort()
!               #matching_distance_count = 0
!               #for rdp_cnt in range(0,len(close_list3)-1):
!               #   rdp1_1 = close_list3[rdp_cnt][0]    # get the path distance betwee these points
!               #   rdp1_2 = close_list3[rdp_cnt+1][0]
!               #
!               #   rdp2_1 = close_list3[rdp_cnt][1]
!               #   rdp2_2 = close_list3[rdp_cnt+1][1]
!               #   
!               #   route_distance1 = path1.get_route_distance(int(path1.feature_loc[rdp1_1,2]), int(path1.feature_loc[rdp1_2,2]))
!               #   route_distance2 = path2.get_route_distance(int(path2.feature_loc[rdp2_1,2]), int(path2.feature_loc[rdp2_2,2]))
!               #
!               #   max_distance = max(route_distance1,route_distance2)
!               #   min_distance = min(route_distance1,route_distance2)
!               #
!               #   if (max_distance/min_distance < 1.25 or max_distance-min_distance < 20):
!               #       matching_distance_count+=1
!               #
!               #if (matching_distance_count < 2):
!               #    path1.print_flag = 1



subroutine max_distance_between_segments(path1_route, path2_route, path1_segment_start, path1_segment_end, path2_segment_start, &
                                         path2_segment_end, N1, N2, maximum_distance)

!f2py   intent(in) :: path1_route
!f2py   intent(in) :: path2_route
!f2py   intent(in) :: path1_segment_start
!f2py   intent(in) :: path1_segment_end
!f2py   intent(in) :: path2_segment_start
!f2py   intent(in) :: path2_segment_end
!
!f2py   intent(out) :: maximum_distance
!
!f2py   intent(hide) :: N1
!f2py   intent(hide) :: N2

   real*8  path1_route(N1,2)
   real*8  path2_route(N2,2)
   integer path1_segment_start, path1_segment_end, path2_segment_start, path2_segment_end 
   real    maximum_distance

   

   integer i,j,k,done, i2
   integer previous_match
   integer path1_start, path1_end, path2_start, path2_end
   integer search_start, search_end
   integer    closest_point
   real    current_distance, min_distance
   real    distance_required,  distance_too_large 
   real    x1, x2, y1, y2
   
   real*8  holding_route1(100000,2)
   real*8  holding_route2(100000,2)
   
   real   x1_hold, y1_hold, x2_hold, y2_hold
   real   x1_hold2, y1_hold2, x2_hold2, y2_hold2
   
   integer holding_start, holding_end
   integer holding_start2, holding_end2
   
   
   
   distance_required = 15   ! the line needs to be within 25 meters
   distance_too_large = 25
   
   
   maximum_distance = 0
   path1_start = min(path1_segment_start+1, path1_segment_end+1)  ! these might come in out of order, we want low to high
   path1_end = max(path1_segment_start+1, path1_segment_end+1)  ! these might come in out of order, we want high to low

   path2_start = min(path2_segment_start+1, path2_segment_end+1)  ! these might come in out of order, we want low to high
   path2_end = max(path2_segment_start+1, path2_segment_end+1)  ! these might come in out of order, we want high to low
   
   
   !write(6,*)  '************ ',path1_start, path1_end, path2_start, path2_end
   
   
   do k=1,2   !* compare route 1 to route 2, then compare route 2 to route 1
   
      if (maximum_distance .lt. distance_too_large) then
   
         if (k .eq. 1) then
            !write(6,*) 'here 15 '
            holding_route1 = 0
            holding_route2 = 0
            holding_route1(1:N1,:) = path1_route
            holding_route2(1:N2,:) = path2_route
            holding_start = path1_start
            holding_end   = path1_end
            holding_start2 = path2_start
            holding_end2   = path2_end
            holding_length = N2
            !write(6,*) 'here 16 '
         else
            !write(6,*) 'here 17 '         
            holding_route1 = 0
            holding_route2 = 0
            holding_route1(1:N2,:) = path2_route
            holding_route2(1:N1,:) = path1_route
            holding_start = path2_start
            holding_end   = path2_end
            holding_start2 = path1_start
            holding_end2   = path1_end            
            holding_length = N1
            !write(6,*) 'here 18 '
         end if
      
         !write(6,*) 'here 14 '
         
         !write(6,*) holding_start, holding_end, n1, n2
         
         !write(6,*) 'here 19 '
         
         previous_match = holding_start2
         
         !write(6,*) 'here 20 '
         
         x1_hold2 = 0
         y1_hold2 = 0 
         x2_hold2 = 0
         y2_hold2 = 0
         
         !write(6,*) 'here 21 '
         
         
         do j = holding_start, holding_end, 5
            
            if (maximum_distance .lt. distance_too_large) then
         
               do i2 = 1,2
                  
                  !write(6,*) '*** here 1'
                  
                  if (i2 .eq. 1) then   ! on the first loop, look at a tight range
                     done = 0
                     min_distance = 999
                     search_start = max(previous_match - 10, 1)   ! start out looking through 40 points
                     search_end   = min(previous_match + 10, int(holding_length) )
                  else if (i2 .eq. 2 .and. done .eq. 0) then
                     search_start = max(holding_start2 - 30, 1)   ! look through all the points
                     search_end   = min(holding_end2 + 30, int(holding_length) )
                     min_distance = 999
                  end if
                  
                  
                  i=search_start

                  x1 = holding_route1(j,1)   
                  y1 = holding_route1(j,2)
                  
                  do while(done .eq. 0 .and. i .le. search_end)
                     

         
                     x2 = holding_route2(i,1)   
                     y2 = holding_route2(i,2)     
                     
                     current_distance = ( (x1-x2)**2 + (y1-y2)**2 )**(.5)    ! find the distance between this point on route A and every point on route B
                     
      
                     if ( current_distance .lt. min_distance) then
                        min_distance = current_distance
                        x1_hold = x1
                        y1_hold = y1
                        x2_hold = x2
                        y2_hold = y2
                        previous_match = i

                        if (current_distance < distance_required) then
                           done = 1
                           min_distance = current_distance
                           previous_match = i
                        end if

                     end if
                        
                     i = i+1
                  end do
                  
               end do
               
               
               if (min_distance .gt. maximum_distance)  then
                  maximum_distance = min_distance
                  x1_hold2 = x1_hold
                  y1_hold2 = y1_hold
                  x2_hold2 = x2_hold
                  y2_hold2 = y2_hold  
               end if

            
            end if
            
         end do   ! end loop through all the points on the line segment

     end if         
  
  end do  !* end loop through both paths
  
  
  !write(6,*) maximum_distance, x1_hold2, y1_hold2, x2_hold2, y2_hold2
   

return
end

